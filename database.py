import sqlite3
from datetime import datetime


def create():
    # Connect to the SQLite database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('my_database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS user')
    cursor.execute('DROP TABLE IF EXISTS message')
    cursor.execute('DROP TABLE IF EXISTS msg')
    cursor.execute('DROP TABLE IF EXISTS file')

    # Create the 'user' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL
        )
    ''')

    # Create the 'msg' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender INTEGER NOT NULL,
            receiver INTEGER NOT NULL,
            msg TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender) REFERENCES user (id),
            FOREIGN KEY (receiver) REFERENCES user (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receiver INTEGER NOT NULL,
            sender INTEGER NOT NULL,
            filepath TEXT NOT NULL,
            FOREIGN KEY (receiver) REFERENCES user (id)
            FOREIGN KEY (sender) REFERENCES user (id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create()
