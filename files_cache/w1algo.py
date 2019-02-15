import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
 
mec_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3']
 
cache_size = 3
H = 0
M = 0
MH = 0
re_use = 0
requests = []
 
 
def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    check_cache(hash_no, url)
 
 
def get_time():
    y = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return y
 
 
def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
 
 
def check_cache(hash_no, url):
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Hash='" + hash_no + "'")
        d = cur.fetchone()
        r = d[0]
        if r == 0:
            fetch_from_source(hash_no, url)
        else:
            fetch_from_cache(hash_no)
 
    except sqlite3.Error as e:
        if con:
            con.rollback()
            print('Error in check_cache: {}'.format(e))
 
    finally:
        if con:
            con.close()
 
 
def fetch_from_source(hash_no, url):
    global M
    cmd = "curl {}".format(url)
    os.system(cmd)
 
    print('calling prepare_db')
 
    prepare_db()
 
    cmd = "echo `curl {}` > /home/mec/cache/{}.html".format(url, hash_no)  # CACHES DATA FROM SOURCE
    os.system(cmd)
    print('-----------------------------------')
    print('Cache Miss')
    print('-----------------------------------')
    M += 1
 
    update_local_database(hash_no)
 
 
def update_local_database(hash_no):
    try:
        global con
        con = sqlite3.connect('cache.db')
        cur = con.cursor()
        cache_time = get_time()
        ip = ip_address()
        path = '/home/mec/cache/{}.html'.format(hash_no)
        data = (hash_no, path, cache_time, ip)
        cur.execute("INSERT INTO CacheTable VALUES(?, ?, ?, ?)", data)
        con.commit()
        cur.execute("SELECT * FROM CacheTable")
        d = cur.fetchall()
 
        for row in d:
            print(row)
 
        update_mec_database(hash_no, path, cache_time, ip)
        con.close()
 
    except sqlite3.Error as e:
        print('Error in update_local_database: {}'.format(e))
 
 
def update_mec_database(hash_no, path, cache_time, host_ip):
    ip = ip_address()
    for i in mec_list:
        if i != ip:
            c = paramiko.SSHClient()
 
            un = 'mec'
            pw = 'password'
            port = 22
 
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py insert "{}" "{}" "{}" "{}"'.format(hash_no, path, cache_time, host_ip)
 
            stdin, stdout, stderr = c.exec_command(cmd)
 
 
def fetch_from_cache(hash_no):
    global H
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Host_ip FROM CacheTable WHERE Hash='" + hash_no + "'")
        host_ip_list = cur.fetchall()
        h_list = []
        for i in host_ip_list:
            h_list.append(i[0])
 
        local_ip = ip_address()
        if local_ip in h_list:
            time = get_time()
            cmd = "cat /home/mec/cache/{}.html".format(hash_no)
            os.system(cmd)
            print('-----------------------------------')
            print('Cache Hit from localhost')
            print('-----------------------------------')
            H += 1
            cur.execute("update CacheTable set DateTime = '" + time + "' where Hash = '" + hash_no + "' and Host_ip = '" + local_ip + "';")
            con.close()
        elif len(host_ip_list) == 1:
            fetch_from_mec(hash_no, host_ip_list[0][0])
 
        elif len(host_ip_list) > 1:
            max_band_ip = get_max_band()
            fetch_from_mec(hash_no, max_band_ip)
 
    except sqlite3.Error as e:
        print('Error in fetch_from_cache: {}'.format(e))
 
 
def fetch_from_mec(hash_no, host_ip):
    global MH
    c = paramiko.SSHClient()
 
    un = 'mec'
    pw = 'password'
    port = 22
 
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host_ip, port, un, pw)
    cmd = 'cat /home/mec/cache/{}.html'.format(hash_no)
 
    stdin, stdout, stderr = c.exec_command(cmd)
 
    prepare_db()
 
    for line in stdout:
        q = len(line) - 1
        t = line[:q]
        cmd = "echo '{}' >> /home/mec/cache/{}.html".format(t, hash_no)
        os.system(cmd)
 
    cmd = 'cat /home/mec/cache/{}.html'.format(hash_no)
    update_local_database(hash_no)
    os.system(cmd)
    print('-----------------------------------')
    print('Cache Hit from MEC')
    print('-----------------------------------')
    MH += 1
 
 
def get_max_band():
    #M1 = '10.1.1.1'
    M2 = '10.2.2.2'
    M3 = '10.3.3.3'
    conn = sqlite3.connect('/home/mec/cache.db')
    curr = conn.cursor()
    sql_cmd = "SELECT M2, M3 FROM Bw_Table ORDER BY Id DESC LIMIT 1;"
    curr.execute(sql_cmd)
    data = curr.fetchone()
    a = data[0]
    b = data[1]
    c = [a, b]
    d = max(c)
    e = c.index(d)
    if e == 0:
        return M2
    elif e == 1:
        return M3
 
 
def prepare_db():
    global re_use
    host_ip = ip_address()
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
 
        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + host_ip + "'")
        d = cur.fetchone()
        r = d[0]  # This value represents how many data entries for host_ip
 
        print('\ntotal items in database is {}'.format(r))
 
        if r >= cache_size:
            cur.execute("SELECT DateTime FROM CacheTable where Host_ip = '" + host_ip + "'")
 
            data = cur.fetchall()  # returns array that looks like [('2018-08-20 13:23:49',), ('2018-08-20 11:56:04',), ('2018-08-20 13:40:01',)]
 
            min_time = min(data)[0]  # Return minimum time
 
            delete_from_mec(min_time, host_ip)
 
            cur.execute(
                "SELECT Hash FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            data = cur.fetchone()
 
            cmd = 'rm /home/mec/cache/{}.html'.format(data[0])
            os.system(cmd)
 
            cur.execute("DELETE FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            con.commit()
 
            con.close()
            re_use += 1
 
            # cur.execute("SELECT * FROM CacheTable")
 
    except sqlite3.Error as e:
        print('Error Encountered in Prepare_db: {}'.format(e))
 
 
def delete_from_mec(min_time, host_ip):
    ip = ip_address()
    for i in mec_list:
        if i != ip:
            c = paramiko.SSHClient()
 
            un = 'mec'
            pw = 'password'
            port = 22
 
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py delete "{}" "{}" '.format(min_time, host_ip)
 
            stdin, stdout, stderr = c.exec_command(cmd)
 
 
def cache_performance():
    global H
    global M
    global MH
    global re_use
    p = int((H / (H + M)) * 100)
    q = int(((H+MH) / (H+MH+M)) * 100)
    print('----------------------------------------------------------')
    print('                   Cache Performance')
    print('----------------------------------------------------------')
    print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, q))
    print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(H, M))
    print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(MH, H + MH))
    print('----------------------------------------------------------')
    print('         Total use of Replacement Algorithm = {}'.format(re_use))
    print('----------------------------------------------------------')
 
 
def run_me():
    global requests
    while True:
        x = input('Enter any key to start OR stop to stop: ')
        if x == 'stop':
            print('-----------------------------------------')
            print('\n Programme Terminated\n')
            print('-----------------------------------------')
            cache_performance()
            print('\n-----------------------------------------')
            print(requests)
            print('\n-----------------------------------------')
            break
        else:
            for i in range(30):
                fr = open('web_test.txt', 'r')
 
                t = fr.readlines()
 
                v = random.randint(0, (len(t)-1))
                requests.append(v)
                get_hash(t[v])
                fr.close()
                time.sleep(3)
 
 
def main():
    run_me()
 
 
if __name__ == "__main__":
    main()
