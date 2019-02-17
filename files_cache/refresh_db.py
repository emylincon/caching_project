import sqlite3
import os


def main():
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.executescript('''DROP TABLE IF EXISTS CacheTable;
            CREATE TABLE CacheTable(Hash varchar(30), Path varchar(70), DateTime varchar(30), Host_ip varchar(16));
            INSERT INTO CacheTable (Hash, Path, DateTime, Host_ip) VALUES('123a11', '/cache/data1.txt', '12:00', '192.168.1.1');
            INSERT INTO CacheTable (Hash, Path, DateTime, Host_ip) VALUES('127b23', '/cache/data2.txt', '12:05', '192.168.1.2');''')

        cache_data = (('124c33', '/cache/data3.txt', '12:06', '192.168.1.3'),
                      ('124d35', '/cache/data4.txt', '12:07', '192.168.1.4'),
                      ('125e43', '/cache/data5.txt', '12:08', '192.168.1.5'))

        cur.executemany("INSERT INTO CacheTable (Hash, Path, DateTime, Host_ip) VALUES(?, ?, ?, ?)", cache_data)

        con.commit()

        cur.execute("SELECT * FROM CacheTable")

        data = cur.fetchall()

        for row in data:
            print(row)
        clear_temp()

    except sqlite3.Error as e:
        if con:
            con.rollback()
            print('Error Encountered: {}'.format(e))

    finally:
        if con:
            con.close()

            
def clear_temp():
    try:
        os.system('rm /home/mec/temp/*')
        os.system('rm /home/mec/cache/*')
    except:
        print('Database is refreshed')


if __name__ == "__main__":
    main()
