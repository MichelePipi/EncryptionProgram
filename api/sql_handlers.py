import sqlite3

FILE_PATH = 'ciphers.sql'

def create_connection() -> sqlite3.Connection:
    return sqlite3.connect(FILE_PATH, check_same_thread=False)


def delete_table(connection: sqlite3.Connection):
    delete_table_query = "DROP TABLE IF EXISTS ciphers"
    connection.execute(delete_table_query)


def create_table(connection: sqlite3.Connection):
    delete_table(connection)
    create_table_query = """
                            CREATE TABLE ciphers(
                            id INTEGER PRIMARY KEY,
                            original VARCHAR(255),
                            ciphered VARCHAR(255),
                            key INTEGER
                        )"""
    connection.execute(create_table_query)


def commit_changes(connection: sqlite3.Connection):
    connection.commit()


def insert_entry(connection: sqlite3.Connection, original,
                 ciphered, key):
    insert_query = f"""
            INSERT INTO ciphers(original, ciphered, key) 
            VALUES ('{original}', '{ciphered}', '{key}')
            """
    connection.execute(insert_query)
    commit_changes(connection=connection)


def locate_entry_from_id(connection: sqlite3.Connection, id) -> (str, str):
    select_query = f'''SELECT * FROM ciphers WHERE ID={id} '''
    results = connection.execute(select_query).fetchone()
    if results is None:
        return (None, None)
    return results