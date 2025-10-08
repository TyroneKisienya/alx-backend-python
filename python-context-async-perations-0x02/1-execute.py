import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, age):
        self.db_name = db_name
        self.age = age
        self.conn = None
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        print('Connected')
        return self.conn
    def __exit__(self, type, value, traceback):
        if conn:
            self.conn.close()
            print('Closed successfully')
        return False 

with ExecuteQuery('users.db', age = 25) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE age < ?', (25,))
    results = cursor.fetchall()
    print('Returned:', results)