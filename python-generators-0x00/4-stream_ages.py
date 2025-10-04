#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
from seed import DB_CONFIG, DB_NAME

def stream_user_ages():
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG['host'],
            port = DB_CONFIG['port'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
            database = DB_NAME
        )

        cursor = conn.cursor()
        cursor.execute('SELECT age FROM user_data')
        for (age,) in cursor:
            yield float(age)
        
        cursor.close()
        conn.close()
    except Error as e:
        print('Query not working', e)
        return

def calculate_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        avg = total_age / count
        print(f'Average age of users {avg: .2f}')
    else:
        print('No users found in database')
