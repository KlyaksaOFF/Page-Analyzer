import os
from datetime import date

import psycopg2
from dotenv import load_dotenv

load_dotenv('../.env')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


try:
    with conn.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
        id serial PRIMARY KEY,
        name text NOT NULL UNIQUE,
        created_at DATE NOT NULL DEFAULT CURRENT_DATE
        );
        '''),
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


def create_url(url):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO urls (name, created_at) 
            VALUES (%s, %s)''', (url, date.today()))
            conn.commit()
    except psycopg2.Error as e:
        print(e)


def select_url():
    try:
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


def detail_url(url_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT id, name, created_at 
            FROM urls WHERE id = %s''', (url_id,))
            row = cursor.fetchone()
            return row
    except psycopg2.Error as e:
        print(e)
        return None


def get_url_checks(url_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT 
            id, status_code, h1, title, description, created_at 
            FROM url_checks WHERE url_id = %s''', (url_id,))
            rows = cursor.fetchall()
            return rows
    except psycopg2.Error as e:
        print(e)
        return []


def insert_url_checks(url_id, status_code, h1, title, description):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO url_checks 
            (url_id, status_code, h1, title, description, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s)''',
                           (url_id, status_code, h1, title,
                            description, date.today()))
            conn.commit()
    except psycopg2.Error as e:
        print(e)
