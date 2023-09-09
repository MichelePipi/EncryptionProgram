import sqlite3

FILE_PATH = 'ciphers.sql'


def create_connection() -> sqlite3.Connection:
    return sqlite3.connect(FILE_PATH, check_same_thread=False)


def delete_table(connection: sqlite3.Connection):
    delete_table_query = "DROP TABLE IF EXISTS ciphers"
    connection.execute(delete_table_query)


def create_table(connection: sqlite3.Connection):
    create_table_query = """CREATE TABLE ciphers(
                            id INTEGER PRIMARY KEY,
                            original VARCHAR(255),
                            ciphered VARCHAR(255)
                        )"""
    connection.execute(create_table_query)


def commit_changes(connection: sqlite3.Connection):
    connection.commit()