import time
import sqlite3
import functools

#### paste your with_db_decorator here

def with_db_connection(func):
    '''your code goes here'''
    '''Down below'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

'''your code goes here'''
'''Down Below'''

def retry_on_failure(retries = 3, delay = 2):
    '''loop'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f'Attempt {attempt}/{retries}')
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f'Error on attempt {attempt}', e)
                    if attempt < retries:
                        print(f'Retrying in {delay} seconds')
                        time.sleep(delay)
            print(f'Operation failed after multiple attempts')
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure(retries=3, delay=2)
@with_db_connection

def fetch_user_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()
####attempt to fetch users with automatic retry on failure

users = fetch_user_with_retry()
print(users)