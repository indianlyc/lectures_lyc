import sqlite3
from itertools import compress
import datetime


def execute(func):
    def f(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self.executor()

    return f

def strict(func):
    def f(self, *args, strict=False, **kwargs):
        func(self, *args, **kwargs)
        if strict:
            self.params = tuple([el.strip("%") for el in self.params])
    return f


class Table:
    def __init__(self, database: str):
        self.database = database
        with sqlite3.connect(database) as connection:
            self.connection = connection
            self.cursor = connection.cursor()
            self._create_table()

    def _create_table(self):
        self._sql_table_init()
        self.cursor.execute(self.s)
        self.connection.commit()

    def _sql_table_init(self):
        raise NotImplementedError()

    def executor(self):
        print(self.query, self.params)
        with sqlite3.connect(self.database) as connection:
            self.connection = connection
            self.cursor = connection.cursor()
            self.cursor.execute(self.query, self.params)
            return self.cursor.fetchall()


class Purchase(Table):

    def _sql_table_init(self):
        self.s = """       
        CREATE TABLE IF NOT EXISTS Purchase (
            id INTEGER PRIMARY KEY,
            price REAL,
            amount REAL,
            good_id INTEGER,
            shop_id INTEGER,
            datetime TEXT,
            FOREIGN KEY(good_id) REFERENCES Good(id),
            FOREIGN KEY(shop_id) REFERENCES Shop(id)
        )"""

    @execute
    def select_statistic(self, datetime_from=None, datetime_to=None, category_id=None, good_id=None, shop_id=None):
        self.query = """
        SELECT Purchase.datetime, Purchase.price, Purchase.amount, Good.good, Category.category, Shop.shop 
        FROM Purchase 
        LEFT JOIN
        Good
        ON Purchase.good_id = Good.id
        LEFT JOIN
        Shop
        ON Purchase.shop_id = Shop.id
        LEFT JOIN
        Category
        ON Good.category_id  = Category.id
        """
        self.params = ()
        if any([datetime_from, datetime_to, category_id, good_id, shop_id]):
            self.query += """WHERE """

            self.query += " AND ".join(compress(["datetime >= ?", "datetime <= ?", "category_id = ?",
                                                 "good_id = ?", "shop_id = ?"],
                                                [datetime_from, datetime_to, category_id, good_id, shop_id]))
            self.params = tuple(compress([datetime_from, datetime_to, category_id, good_id, shop_id],
                                         [datetime_from, datetime_to, category_id, good_id, shop_id]))

    @execute
    def insert(self, price, amount, good_id, shop_id, dt):
        self.query = """INSERT INTO Purchase (price, amount, good_id, shop_id, datetime) 
                        VALUES (?, ?, ?, ?, ?)"""
        self.params = (price, amount, good_id, shop_id, dt)


class Category(Table):
    def _sql_table_init(self):
        self.s = """       
        CREATE TABLE IF NOT EXISTS Category (
            id INTEGER PRIMARY KEY,
            category TEXT
        )"""

    @execute
    @strict
    def select_by_part(self, part, good_id=None):
        if good_id is not None:
            self.query = """
            SELECT * FROM Category WHERE id in
            (SELECT category_id FROM Good WHERE id = ?)
            """
            self.params = (f'{good_id}')
        else:
            self.query = """
            SELECT id, category FROM Category WHERE category like ?
            """
            self.params = (f'%{part}%',)

    @execute
    def insert(self, val):
        self.query = """
        INSERT INTO Category (category) 
                        VALUES (?)
        """
        self.params = (val,)


class Shop(Table):
    def _sql_table_init(self):
        self.s = """       
        CREATE TABLE IF NOT EXISTS Shop (
            id INTEGER PRIMARY KEY,
            shop TEXT
        )"""

    @execute
    @strict
    def select_by_part(self, part):
        self.query = """
        SELECT id, shop FROM Shop WHERE shop like ?
        """
        self.params = (f'%{part}%',)

    @execute
    def insert(self, val):
        self.query = """
        INSERT INTO Shop (shop) 
                        VALUES (?)
        """
        self.params = (val,)


class Good(Table):
    def _sql_table_init(self):
        self.s = """       
        CREATE TABLE IF NOT EXISTS Good (
            id INTEGER PRIMARY KEY,
            good TEXT,
            category_id INTEGER,
            FOREIGN KEY(category_id) REFERENCES Category(id)
        )"""

    @execute
    @strict
    def select_by_part(self, part):
        self.query = """
        SELECT Good.id, Good.good, Good.category_id, Category.category 
        FROM Good
        LEFT JOIN
        Category
        ON Good.category_id = Category.id
        WHERE good like ?
        """
        self.params = (f'%{part}%',)

    @execute
    def insert(self, good, category_id):
        self.query = """
        INSERT INTO Good (good, category_id) 
                        VALUES (?, ?)
        """
        self.params = (good, category_id)


class App:
    def __init__(self, database):
        self.p = Purchase(database)
        self.c = Category(database)
        self.s = Shop(database)
        self.g = Good(database)

    def add_purchase(self, price, amount, good_id, shop_id, dt=None):
        """
        Выбирать продукт из таблицы Good по части названия
        Вносить новый продукт в таблицу Good
        И аналогично для категории и для магазина
        """
        if dt is None:
            dt = datetime.datetime.now().isoformat()
        self.p.insert(price, amount, good_id, shop_id, dt)

    def get_statistic(self, datetime_from=None, datetime_to=None, category_id=None, good_id=None, shop_id=None):
        """
        Выбор из таблицу Purchase строчек отвечающих данным параметрам
        """
        return self.p.select_statistic(datetime_from, datetime_to, category_id, good_id, shop_id)

    def get_good(self, good_part, **kwargs):
        """
        Возвращает все продукты имена которых совпадают по названию
        """
        return self.g.select_by_part(good_part, **kwargs)

    def get_category(self, category_part, good_id=None, **kwargs):
        return self.c.select_by_part(category_part, good_id, **kwargs)

    def get_shop(self, shop_part, **kwargs):
        return self.s.select_by_part(shop_part, **kwargs)

    def new_good(self, good, category_id):
        return self.g.insert(good, category_id)

    def new_category(self, category):
        return self.c.insert(category)

    def new_shop(self, shop_part):
        return self.s.insert(shop_part)