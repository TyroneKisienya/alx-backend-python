#!/usr/bin/python3

import os
import csv
import uuid

from decimal import Decimal, InvalidOperation

import mysql.connector
from mysql.connector import Error

DB_NAME = 'ALX_prodev'
CSV_FILE = 'user_data.csv'

DB_CONFIG = {
    "host":os.environ.get('MYSQL_HOST', 'localhost'),
    "port":int(os.environ.get('SERVERPORT', 3306)),
    "user":os.environ.get('MYSQL_USER', 'ALX'),
    "password":os.environ.get('MYSQL_PASSWORD', 'password'),
}

def connect_db():
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG['host'],
            port = DB_CONFIG['port'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
        )
        print('Connection successful')
        return conn
    except Error as e:
        print('Connection unsuccessful', e)
        raise

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'
        )
        cursor.close()
        print(f'{DB_NAME} created successfully')
    except Error as e:
        print(f'{DB_NAME} not created', e)
        raise

def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG['host'],
            port = DB_CONFIG['port'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
            database = DB_NAME,
        )
        print(f'{DB_NAME} Database connection successful')
        return conn
    except Error as e:
        print(f'{DB_NAME} Database connection unsuccessful', e)
        raise

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS user_data(
            user_id char(50) PRIMARY KEY NOT NULL,
            name varchar(100) NOT NULL,
            email varchar(250) NOT NULL,
            age decimal (5,2) NOT NULL
            );'''
        )
        cursor.close()
        print('Table created successfully')
    except Error as e:
        print('Script unsuccessful')
        raise

def insert_data(connection, data):
    if isinstance(data, str):
        data = read_csv(data)
    inserted = 0
    select_sql = 'SELECT 1 FROM user_data WHERE user_id = %s'
    insert_sql = 'INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)'

    cursor = connection.cursor()
    for row in data:
        user_id = (row.get('user_id') or '').strip()
        name = (row.get('name') or '').strip()
        email = (row.get('email') or '').strip()
        age = (row.get('age') or '').strip()

        if not user_id:
            user_id = str(uuid.uuid4())
        
        if not name or not email:
            print(f'Skipping the row {row} with missing values')
            continue
        cursor.execute(select_sql, (user_id,))
        if cursor.fetchone():
            continue

        try:
            cursor.execute(insert_sql, (user_id, name, email, age))
            inserted += 1
        except Error as e:
            print('Failed to insert row:', e)

    connection.commit()
    cursor.close()
    print(f'Inserted {inserted} new rows')
    return inserted

def read_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f'CSV file not found on {path}')
    
    rows = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
        return rows
    
def main():
    # 1) Connect to server
    conn = connect_db()

    # 2) Ensure database exists
    create_database(conn)
    conn.close()

    # 3) Connect to the specific database
    db_conn = connect_to_prodev()

    # 4) Ensure table exists
    create_table(db_conn)

    # 5) Read CSV
    try:
        data = read_csv(CSV_FILE)
    except Exception as e:
        print("Could not read CSV:", e)
        db_conn.close()
        return

    # 6) Insert rows
    insert_data(db_conn, data)

    db_conn.close()
    print("Done.")


if __name__ == "__main__":
    main()