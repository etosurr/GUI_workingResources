import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('resources.db')
        self.exemplar = self.conn.cursor()
        self.exemplar.execute('''CREATE TABLE IF NOT EXISTS resources (id integer primary key, description text, costs text, total real)''')
        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.conn.execute('''INSERT INTO resources(description, costs, total) VALUES (?, ?, ?)''',
                          (description, costs, total))
        self.conn.commit()

