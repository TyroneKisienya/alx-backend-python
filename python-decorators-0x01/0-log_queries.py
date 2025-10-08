import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

"""YOUR CODE GOES HERE"""
'''Down below'''
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        log_time = datetime.now()
        print(f'Executing query:{query} at {log_time}')
        return func(query, *args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query= 'SELECT * FROM users')