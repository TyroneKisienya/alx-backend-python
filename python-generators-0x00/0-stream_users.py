#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import sys
from seed import DB_CONFIG, DB_NAME

def stream_users():
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG ['host'],
            port = DB_CONFIG ['port'],
            user = DB_CONFIG ['user'],
            password = DB_CONFIG ['password'],
            database = DB_NAME
        )
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT  * FROM user_data;')

        for row in cursor:
            yield row
        cursor.close()
        conn.close()

    except Error as e:
        print('Error fetching data', e)
        return

sys.modules[__name__] = stream_users