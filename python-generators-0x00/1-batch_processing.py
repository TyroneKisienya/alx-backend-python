#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
from seed import DB_CONFIG, DB_NAME

def stream_users_in_batches(batch_size):
    try:
        conn = mysql.connector.connect(
            host = DB_CONFIG['host'],
            port = DB_CONFIG['port'],
            user = DB_CONFIG['user'],
            password = DB_CONFIG['password'],
            database = DB_NAME
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_data')

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
            if batch:
                yield batch
        cursor.close()
        conn.close()
    
    except Error as e:
        print('Error fetching batch', e)

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if float(user['age']) > 25]
        print(f'processed batch with {len(filtered)} users over 25')
        yield filtered
    return