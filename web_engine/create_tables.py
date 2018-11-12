import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username text,
        password text
    )
"""
cursor.execute(create_users)

create_items = """
    CREATE TABLE IF NOT EXISTS items (
        name text,
        price real
    )
"""
cursor.execute(create_items)

insert_items = "INSERT INTO items VALUES ('test', 12.7)"
cursor.execute(insert_items)

connection.commit()
connection.close()
