from .database import get_db_connection
import psycopg2
def init_db():
    try:
        conn = get_db_connection()
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
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()