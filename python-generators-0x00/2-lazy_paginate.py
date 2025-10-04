#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
from seed import DB_NAME, DB_CONFIG

def paginate_users(page_size, offset):
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG['host'],
            port = DB_CONFIG['port'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
            database = DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}')
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows
    except Error as e:
        print('error lazy load, try again', e)
        return []

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size