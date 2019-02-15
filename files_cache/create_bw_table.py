import sqlite3
 
 
def main():
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.executescript('''DROP TABLE IF EXISTS Bw_Table;
            CREATE TABLE Bw_Table(Id integer not null primary key, M2 varchar(50), M3 varchar(50));
            INSERT INTO Bw_Table VALUES(1, 'test1', 'test2');
            ''')
        con.commit()
 
        cur.execute("SELECT * FROM Bw_Table")
 
        data = cur.fetchall()
 
        for row in data:
            print(row)
 
    except sqlite3.Error as e:
        if con:
            con.rollback()
            print('Error Encountered: {}'.format(e))
 
    finally:
        if con:
            con.close()
 
 
if __name__ == "__main__":
    main()
