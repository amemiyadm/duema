import sqlite3

connection = sqlite3.connect('sqlite/database.db')

with open('sqlite/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
