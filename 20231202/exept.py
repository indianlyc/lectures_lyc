import sqlite3

with sqlite3.connect("my_database") as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Purchase", ())
    print(cursor.fetchall())