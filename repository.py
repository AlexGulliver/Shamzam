import sqlite3

class Repository:
    def __init__(self, table):
        self.table = table
        self.database = self.table + ".db"
        self.make()

    def make(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table} " +
                "(code TEXT PRIMARY KEY, name TEXT)"
            )
            connection.commit()

    def clear(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table}"
            )
            connection.commit()

    def insert(self, js):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.table} (code,name) VALUES (?,?)",
                (js["code"], js["name"])
            )
            connection.commit()
            return cursor.rowcount
        
    def update(self, js):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE {self.table} SET name=? WHERE code=?",
                (js["name"], js["code"])
            )
            connection.commit()
            return cursor.rowcount
        
    def lookup(self, code):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT code, name FROM {self.table} WHERE code=?",
                (code,)
            )
            row = cursor.fetchone()
            if row:
                return {"code":row[0], "name":row[1]}
            else:
                return None
