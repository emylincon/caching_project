import sqlite3
import random as r
import pandas as pd


class Database:
    def __init__(self, name='util.db'):
        self.db = name
        self.count = 0
        self.columns = ['Id', 'Memory', 'CPU', 'RTT']
        self.create_table()

    def get_con(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        return con, cur

    def create_table(self):
        con, cur = self.get_con()
        cur.executescript('''DROP TABLE IF EXISTS Utilization;
                    CREATE TABLE Utilization(Memory REAL, CPU REAL, RTT REAL);''')
        con.commit()
        con.close()

    def insert(self, mem, cpu, rtt):
        con, cur = self.get_con()
        cur.execute("INSERT INTO Utilization(Memory, CPU, RTT) VALUES(?, ?, ?)", (mem, cpu, rtt))
        con.commit()
        con.close()
        self.count += 1

    def select_limit(self, limit=200):
        if self.count <= limit:
            return self.select_all()
        else:
            offset = self.count - limit
            con, cur = self.get_con()
            cur.execute(f"SELECT rowid, Memory, CPU, RTT FROM Utilization LIMIT {limit} OFFSET {offset};")
            data = cur.fetchall()
            self.display(data)
            con.close()
            return self.format_data(data)

    @staticmethod
    def display(data):
        for ind in range(len(data)):
            print(data[ind])

    def format_data(self, data):
        df = pd.DataFrame(data, columns=self.columns)
        return df.to_dict()

    def select_all(self):
        con, cur = self.get_con()
        cur.execute("SELECT rowid, Memory, CPU, RTT FROM Utilization")
        data = cur.fetchall()
        self.display(data)
        con.close()
        return self.format_data(data)


# db = Database()
# for i in range(20):
#     a = tuple([round(r.uniform(20,50),3) for j in range(3)])
#     db.insert(*a)
#
# db.select_all()
# print('-'*100)
# db.select_limit(limit=5)
