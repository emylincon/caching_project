import sqlite3
 
con = sqlite3.connect('/home/mec/cache.db')
cur = con.cursor()
 
cur.execute("delete FROM CacheTable WHERE Host_ip in ('10.1.1.1', '10.2.2.2', '10.3.3.3')")
con.commit()
 
cur.execute("select * from CacheTable")
data = cur.fetchall()
 
for row in data:
    print(row)
 
con.close()
