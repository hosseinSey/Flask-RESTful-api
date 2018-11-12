import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Create table
query_creat_table = """
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, username text, password text)
"""
cursor.execute(query_creat_table)

# Insert values
query_add_user = """
    INSERT INTO users VALUES (NULL, ?, ?)
"""
users = [
    ("Ali", 'asdf'),
    ("Hassan", "qwert"),
]
cursor.executemany(query_add_user, users)

# Read values
query_select_all = """
    SELECT * FROM users
"""
users = list(cursor.execute(query_select_all))


connection.commit()
connection.close()
