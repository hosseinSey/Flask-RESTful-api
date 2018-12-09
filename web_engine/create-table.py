import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

query_create_table = """
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username text, password text)
"""
cursor.execute(query_create_table)

query_insert_user = "INSERT INTO users VALUES (?, ?, ?)"
user = (1, 'hossein', 'pass')
cursor.execute(query_insert_user, user)

users = [
    (2, 'Ali', 'asdf'),
    (3, 'hassan', 'qwer')
]
cursor.executemany(query_insert_user, users)

query_select = "SELECT * FROM users"
users = list(cursor.execute(query_select))

for u in users:
    print(u)

query = """
    CREATE TABLE IF NOT EXISTS items
    (id INTEGER PRIMARY KEY, name text, price real)
"""
cursor.execute(query)

connection.commit()
connection.close()
