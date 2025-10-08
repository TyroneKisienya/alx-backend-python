import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        print(f'Connected')
        return self.conn
    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()
            print(f'Closed Successfully')
        return False
    
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    query = 'SELECT * from users'
    cursor.execute(query)
    results = cursor.fetchall()
    print(f'Query results:', results)