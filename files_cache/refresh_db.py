import sqlite3
import os
 
con = sqlite3.connect('/home/mec/cache.db')
cur = con.cursor()
 
cur.execute("delete FROM CacheTable WHERE Host_ip in ('192.168.40.137', '10.0.0.10', '10.0.0.20', '10.0.0.30')")
con.commit()
 
cur.execute("select * from CacheTable")
data = cur.fetchall()
 
for row in data:
    print(row)
 
con.close()

os.system('rm /home/mec/cache/*.html')
