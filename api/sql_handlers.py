import sqlite3


# CONSTANTS
FILE_PATH = 'ciphers.sql'
CONNECTION = sqlite3.connect(FILE_PATH, check_same_thread=False)


def create_cursor() -> sqlite3.Cursor:
    return CONNECTION.cursor()


def delete_table(cursor: sqlite3.Cursor):
    delete_table_query = "DROP TABLE IF EXISTS ciphers"
    cursor.execute(delete_table_query)
    CONNECTION.commit()


def create_table():
    cursor = create_cursor()
    # delete_table(cursor)
    create_table_query = """
                            CREATE TABLE IF NOT EXISTS ciphers(
                            id INTEGER PRIMARY KEY,
                            original VARCHAR(255),
                            ciphered VARCHAR(255),
                            key INTEGER
                        )"""
    cursor.execute(create_table_query) # Create table
    close_cursor(cursor)
    CONNECTION.commit() # Commit changes


def insert_entry(original, ciphered, key):
    cursor = create_cursor()
    insert_query = f"""
            INSERT INTO ciphers(original, ciphered, key) 
            VALUES ('{original}', '{ciphered}', '{key}')
            """ # Build up query to execute
    cursor.execute(insert_query)
    id_of_insert = cursor.lastrowid
    close_cursor(cursor)
    CONNECTION.commit()
    return id_of_insert # Return id of insertion to display back to user


def locate_entry_from_id(entry_id) -> (str, str):
    cursor = create_cursor()
    select_query = f'''SELECT * FROM ciphers WHERE id={entry_id} '''
    print(select_query)
    results = cursor.execute(select_query).fetchone()
    print(results)

    if results is None:
        return (None, None)
    close_cursor(cursor)
    return results


def close_cursor(cursor: sqlite3.Cursor) -> None:
    cursor.close()
