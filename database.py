# database.py

import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS publications (
        id INTEGER PRIMARY KEY,
        pmcid TEXT NOT NULL,
        title TEXT,
        abstract TEXT,
        pub_date TEXT,
        corresponding_author TEXT,
        corresponding_author_email TEXT,
        author_list TEXT,
        affiliations_list TEXT,
        pubmed_id TEXT,
        url TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_publication(conn, publication):
    sql = '''
    INSERT INTO publications(pmcid, title, abstract, pub_date, corresponding_author, corresponding_author_email, author_list, affiliations_list, pubmed_id, url)
    VALUES(?,?,?,?,?,?,?,?,?,?)
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, publication)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

