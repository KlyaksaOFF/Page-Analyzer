import os
from datetime import date

import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set in environment variables")

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    return conn


def init_db():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
            id serial PRIMARY KEY,
            name text NOT NULL UNIQUE,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE
            );
            ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS url_checks (
            id serial PRIMARY KEY,
            url_id int NOT NULL REFERENCES urls(id) ON DELETE CASCADE,
            status_code text,
            h1 text,
            title text,
            description text,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE);''')
            conn.commit()
            print('Таблица создана')
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def create_url(url):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO urls (name, created_at) 
            VALUES (%s, %s) RETURNING ID''', (url, date.today()))
            url_id = cursor.fetchone()[0]
            conn.commit()
            return url_id
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def select_url():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    urls.id, 
                    urls.name, 
                    urls.created_at,
                    MAX(url_checks.created_at) as last_check_date,
                    (SELECT status_code 
                     FROM url_checks 
                     WHERE url_id = urls.id 
                     ORDER BY created_at DESC 
                     LIMIT 1) as last_status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id
                ORDER BY urls.created_at DESC
            ''')
            rows = cursor.fetchall()
            return rows
    except psycopg2.Error as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()


def detail_url(url_id):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''SELECT id, name, created_at 
            FROM urls WHERE id = %s''', (url_id,))
            row = cursor.fetchone()
            return row
    except psycopg2.Error as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()


def get_url_checks(url_id):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''SELECT 
            id, status_code, h1, title, description, created_at 
            FROM url_checks WHERE url_id = %s''', (url_id,))
            rows = cursor.fetchall()
            return rows
    except psycopg2.Error as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()


def insert_url_checks(url_id, status_code, h1, title, description):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO url_checks 
            (url_id, status_code, h1, title, description, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s)''',
                           (url_id, status_code, h1, title,
                            description, date.today()))
            conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


def find_by_url_name(name):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM urls WHERE name = %s", (name,))
            row = cursor.fetchone()
            if row:
                return {'id': row[0], 'name': row[1]}
            return None
    finally:
        if conn:
            conn.close()