import sqlite3
from flask import current_app


def init_db():
    db = sqlite3.connect(current_app.config["DATABASE"])
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
        )
        """)
    db.commit()
    db.close()

# создаём или открываем базу данных
# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()
#
# # создаём таблицу users
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT NOT NULL UNIQUE,
#     password_hash TEXT NOT NULL
# )
# """)
#
# # сохраняем изменения
# conn.commit()
# conn.close()
