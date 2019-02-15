import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
 
mec_list = ['10.0.0.10', '10.0.0.20', '10.0.0.30']
 
cache_size = 3
H = 0
M = 0
MH = 0
re_use = 0
ref = [2, 6, 4, 1, 2, 6, 3, 2, 0, 3, 4, 2, 6, 1, 5, 6, 2, 5, 2, 6, 4, 5, 6, 3, 6, 4, 0, 4, 4, 6]
 
freq = {}
window_size = 0
 
 
def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    calc_relative_freq(hash_no)
    check_cache(hash_no, url)
 
 
def calc_relative_freq(x):
    global freq
    global window_size
 
    window_size += 1
    alpha = 1 / window_size
    delta = alpha / (len(freq) + 1)
    if x not in freq.keys():
        for k in freq.keys():
            freq[k] -= delta
        freq[x] = alpha
    else:
        for k in freq.keys():
            if k != x:
                freq[k] -= delta
        freq[x] += (len(freq) - 1) * delta
 
 
def get_time():
    y = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return y
 
 
def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.1", 80))
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
 
    prepare_db()  # CHECKS IF CACHE IS FULL AND ELIMINATES VICTIM
 
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
        print('Error in cache_update: {}'.format(e))
 
 
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
    try:
        global con
        global H
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
        print('Error in cache_update: {}'.format(e))
 
 
def frequently_used(hash_no):
    host_ip = ip_address()
    global freq
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Hash FROM CacheTable WHERE Host_ip ='" + host_ip + "'")
        host_ip_list = cur.fetchall()
        li = []
        for i in range(len(host_ip_list)):
            li.append(host_ip_list[i - 1][0])
        fre_li = []
        for i in li:
            fre_li.append(freq[i])
        min_freq = min(fre_li)
 
        if min_freq > freq[hash_no]:
            return 'no'
        elif min_freq < freq[hash_no]:
            y = fre_li.index(min_freq)
            delete_least_frequent_mec(li[y], host_ip)
            delete_least_frequent_locally(li[y], host_ip)
            return 'yes'
 
    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))
 
 
def delete_least_frequent_locally(hash_no, host_ip):
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("DELETE FROM CacheTable WHERE Hash = '" + hash_no + "' AND Host_ip = '" + host_ip + "'")
        con.commit()
        con.close()
        cmd = 'rm /home/mec/cache/{}.html'.format(hash_no)
        os.system(cmd)
 
    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))
 
 
def delete_least_frequent_mec(hash_no, host_ip):
    for i in mec_list:
        if i != host_ip:
            c = paramiko.SSHClient()
 
            un = 'mec'
            pw = 'password'
            port = 22
 
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = 'python3 /home/mec/db_manage.py del "{}" "{}" '.format(hash_no, host_ip)
 
            stdin, stdout, stderr = c.exec_command(cmd)
 
 
def fetch_from_mec(hash_no, host_ip):
    c = paramiko.SSHClient()
    global MH
    global re_use
 
    un = 'mec'
    pw = 'password'
    port = 22
 
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host_ip, port, un, pw)
    cmd = 'cat /home/mec/cache/{}.html'.format(hash_no)
 
    stdin, stdout, stderr = c.exec_command(cmd)
 
    con = sqlite3.connect('/home/mec/cache.db')
    cur = con.cursor()
 
    ip = ip_address()
 
    cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + ip + "'")
    d = cur.fetchone()
    r = d[0]  # This value represents how many data entries for host_ip
 
    if r >= cache_size and frequently_used(hash_no) == 'no':
        for line in stdout:
            q = len(line) - 1
            t = line[:q]
            print(t)
        print('-----------------------------------')
        print('Hit from MEC Not Cached')
        print('-----------------------------------')
        MH += 1
    else:
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
        if r >= cache_size:
            re_use += 1
    con.close()
 
 
def get_max_band():
    #M1 = '10.1.1.1'
    M2 = '10.0.0.20'
    M3 = '10.0.0.30'
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
        print('Error Encountered: {}'.format(e))
 
 
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
    global window_size
    global re_use
    p = int((H / 30) * 100)
    q = int(((H+MH) / 30) * 100)
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
    while True:
        print('\n')
        s = input('Enter any key to start and stop to exit: ')
        if s == 'stop':
            print('\nProgramme Terminated')
            print(freq)
            cache_performance()
            break
        else:
            '''
            for i in range(30):
                fr = open('web_test.txt', 'r')
 
                t = fr.readlines()
 
                v = random.randint(0, (len(t) - 1))
                get_hash(t[v])
                fr.close()
                time.sleep(3)
            '''
            for v in ref:
                fr = open('web_test.txt', 'r')
 
                t = fr.readlines()
                get_hash(t[v])
                fr.close()
                time.sleep(3)
 
 
def main():
    run_me()
 
 
if __name__ == "__main__":
    main()
