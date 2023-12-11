import sys
# import os
# os.environ["QT_PLUGIN_PATH"] = "/usr/lib/qt/plugins"

from PyQt5 import QtWidgets, uic, QtCore
from module import App

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return len(self.data[0])

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.data[index.row()][index.column()])


database_name = "my_database"
my_app = App(database_name)

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("main.ui")

def save_purschase():
    price = float(window.price_edit.text())
    amount = float(window.amount_edit.text())
    good = window.good_edit.text()
    category = window.category_edit.text()
    shop = window.shop_edit.text()
    dt = window.datetime_edit.dateTime().toPyDateTime().isoformat()
    res = my_app.get_shop(shop, strict=True)
    if not res:
        my_app.new_shop(shop)
        res = my_app.get_shop(shop, strict=True)
    shop_id, _ = res[0]

    res = my_app.get_category(category, strict=True)
    if not res:
        my_app.new_category(category)
        res = my_app.get_category(category, strict=True)
    category_id, _ = res[0]

    res = my_app.get_good(good, strict=True)
    if not res:
        my_app.new_good(good, category_id)
        res = my_app.get_good(good, strict=True)
    print(res)
    good_id, _, _, _ = res[0]

    print(price, amount, good, good_id, shop, shop_id, category, category_id, dt)
    my_app.add_purchase(price, amount, good_id, shop_id, dt)

    data = my_app.get_statistic()
    print(data)
    model = TableModel(data)
    window.table_view.setModel(model)

window.add_button.clicked.connect(save_purschase)

window.show()
app.exec()