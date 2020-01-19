import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
import subprocess as sp
import ast
from threading import Thread
from pyfiglet import Figlet
import numpy

__author__ = 'Emmanuel'
# mec_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3']

cache_size = 4
H = 0
M = 0
MH = 0
re_use = 0
# ref = [1, 3, 5, 6, 4, 5, 1, 5, 5, 4, 0, 2, 0, 2, 0, 1, 4, 6, 6, 1, 0, 4, 2, 3, 1, 3, 6, 4, 3, 3]
# ref = [1, 5, 0, 3, 14, 7, 4, 17, 11, 19, 10, 7, 19, 9, 14, 2, 18, 0, 6, 2, 12, 11, 12, 10, 17, 9, 10, 7, 12, 6, 0, 6, 0, 5, 10, 17, 18, 8, 5, 0, 8, 8, 14, 4, 4, 0, 0, 14, 10, 14, 10, 15, 9, 7, 17, 6, 18, 2, 2, 18, 8, 1, 11, 14, 13, 3, 0, 5, 19, 6, 10, 0, 7, 8, 3, 3, 18, 10, 19, 6, 7, 9, 6, 10, 7, 9, 8, 15, 19, 17, 15, 15, 7, 2, 7, 17, 6, 9, 16, 9, 18, 16, 15, 18, 15, 5, 3, 4, 10, 14, 10, 9, 12, 16, 8, 3, 15, 3, 17, 6, 13, 13, 8, 8, 8, 10, 11, 13, 19, 0, 5, 19, 15, 5, 11, 14, 12, 10, 5, 2, 17, 8, 1, 11, 16, 5, 9, 6, 14, 11, 15, 14, 8, 8, 8, 18, 10, 12, 3, 17, 0, 13, 4, 18, 5, 19, 13, 19, 4, 12, 0, 16, 2, 16, 19, 0, 6, 13, 15, 12, 5, 16, 1, 16, 0, 9, 9, 1, 5, 14, 1, 6, 11, 2, 12, 5, 8, 19, 1, 9, 7, 2, 11, 15, 7, 2, 17, 14, 13, 16, 14, 2, 17, 10, 12, 14, 18, 1, 7, 8, 6, 7, 3, 18, 18, 9, 12, 6, 18, 16, 1, 16, 13, 9, 2, 8, 6, 14, 14, 14, 9, 5, 0, 18, 17, 15, 9, 2, 15, 7, 4, 18, 14, 11, 3, 1, 12, 17, 0, 15, 8, 12, 1, 8, 8, 18, 13, 11, 3, 5, 11, 18, 10, 15, 10, 3, 3, 7, 1, 13, 18, 5, 9, 7, 10, 6, 17, 14, 10, 10, 15, 7, 11, 16, 4, 4, 9, 2, 5, 14, 0, 2, 13, 19, 1, 10, 16, 16, 7, 10, 0, 4, 18, 5, 0, 19, 1, 0, 16, 0, 6, 9, 10, 6, 0, 17, 14, 6, 10, 1, 0, 9, 9, 10, 10, 11, 3, 15, 15, 5, 17, 19, 8, 2, 4, 3, 7, 7, 17, 8, 18, 5, 12, 12, 2, 14, 5, 17, 2, 10, 13, 13, 17, 7, 15, 19, 3, 8, 14, 16, 11, 12, 13, 3, 7, 11, 10, 17, 19, 11, 8, 14, 7, 15, 17, 14, 8, 15, 10, 19, 9, 9, 13, 14, 18, 7, 4, 13, 18, 16, 10, 7, 8, 13, 8, 16, 8, 11, 9, 9, 9, 2, 1, 0, 0, 17, 16, 4, 16, 4, 17, 2, 16, 5, 12, 4, 17, 6, 7, 9, 6, 17, 14, 18, 1, 8, 18, 0, 19, 16, 5, 2, 17, 18, 18, 2, 17, 4, 0, 16, 0, 9, 14, 13, 3, 9, 1, 13, 19, 18, 9, 7, 4, 15, 2, 5, 4, 7, 3, 9, 4, 3, 4, 7, 3, 18, 6, 2, 17, 3, 10, 0, 19, 19, 5, 6, 18, 9, 6, 3, 10, 7, 1, 0, 5, 12, 6, 15, 1, 8]
ref = [1, 5, 9, 9, 9, 7, 9, 17, 9, 19, 10, 9, 19, 9, 14, 2, 18, 0, 6, 2, 9, 9, 10, 10, 17, 9, 10, 7, 12, 6, 0, 6, 0, 5,
       10, 17, 18, 8, 8, 0, 8, 8, 14, 4, 4, 0, 0, 14, 10, 14, 10, 15, 9, 7, 17, 6, 18, 2, 2, 18, 8, 1, 9, 14, 13, 3, 0,
       5, 19, 6, 10, 0, 7, 8, 3, 3, 18, 10, 19, 6, 7, 9, 6, 10, 7, 9, 8, 15, 19, 17, 15, 15, 7, 2, 7, 17, 6, 9, 16, 9,
       18, 16, 15, 18, 15, 5, 3, 4, 10, 14, 10, 9, 10, 16, 8, 3, 15, 3, 17, 6, 13, 13, 8, 8, 8, 10, 8, 13, 19, 0, 5, 19,
       15, 5, 9, 14, 12, 10, 5, 2, 17, 8, 1, 11, 16, 5, 9, 6, 14, 11, 15, 14, 8, 8, 8, 18, 10, 12, 3, 17, 0, 13, 4, 18,
       5, 19, 13, 19, 4, 12, 0, 16, 2, 16, 19, 0, 6, 13, 15, 12, 5, 16, 1, 16, 0, 9, 9, 1, 5, 14, 1, 6, 11, 2, 12, 5, 8,
       19, 1, 9, 7, 2, 9, 15, 7, 2, 17, 14, 13, 16, 14, 2, 17, 10, 12, 14, 18, 1, 7, 8, 6, 7, 3, 18, 18, 9, 12, 6, 18,
       16, 1, 16, 13, 9, 2, 8, 6, 14, 14, 14, 9, 5, 0, 18, 17, 15, 9, 2, 15, 7, 4, 18, 14, 9, 3, 1, 12, 17, 0, 15, 8,
       12, 1, 8, 8, 18, 13, 11, 3, 5, 11, 18, 10, 15, 10, 3, 3, 7, 1, 13, 18, 5, 9, 7, 10, 6, 17, 14, 10, 10, 15, 7, 11,
       16, 4, 4, 9, 2, 5, 14, 0, 2, 13, 19, 1, 10, 16, 16, 7, 10, 0, 4, 18, 5, 0, 19, 1, 0, 16, 0, 6, 9, 10, 6, 0, 17,
       14, 6, 10, 1, 0, 9, 9, 10, 10, 11, 3, 15, 15, 5, 17, 19, 8, 2, 4, 3, 7, 7, 17, 8, 18, 5, 10, 10, 2, 14, 5, 17, 2,
       10, 13, 13, 17, 7, 15, 19, 3, 8, 14, 16, 11, 10, 13, 3, 7, 11, 10, 17, 19, 11, 8, 14, 7, 15, 17, 14, 8, 15, 10,
       19, 9, 9, 13, 14, 18, 7, 4, 13, 18, 16, 10, 7, 8, 13, 8, 16, 8, 11, 9, 9, 9, 2, 1, 0, 0, 17, 16, 4, 16, 4, 17, 2,
       16, 5, 1, 4, 17, 6, 7, 9, 6, 17, 14, 18, 1, 8, 18, 0, 19, 16, 5, 2, 17, 18, 18, 2, 17, 4, 0, 16, 0, 9, 14, 13, 3,
       9, 1, 13, 19, 18, 9, 7, 4, 15, 2, 5, 4, 7, 3, 9, 4, 3, 4, 7, 3, 18, 6, 2, 17, 3, 10, 0, 19, 19, 5, 6, 18, 9, 6,
       3, 10, 7, 1, 0, 5, 12, 6, 15, 1, 8]
# ref = [19, 13, 4, 16, 4, 15, 5, 9, 15, 16, 17, 13, 11, 2, 2, 15, 8, 17, 14, 3, 10, 8, 0, 19, 2, 14, 2, 10, 8, 19, 18, 17, 14, 10, 3, 4, 9, 2, 8, 7, 13, 6, 8, 3, 17, 9, 18, 11, 10, 11, 11, 0, 8, 13, 19, 18, 4, 13, 9, 13, 5, 7, 2, 13, 14, 19, 19, 2, 13, 6, 12, 3, 14, 17, 3, 5, 17, 0, 11, 12, 6, 10, 10, 12, 0, 17, 5, 6, 8, 15, 8, 6, 0, 15, 7, 13, 3, 0, 8, 5, 4, 10, 9, 10, 9, 16, 15, 9, 3, 11, 8, 3, 3, 18, 18, 4, 2, 16, 19, 17, 17, 17, 4, 4, 11, 12, 5, 16, 13, 8, 1, 11, 13, 11, 18, 0, 6, 10, 15, 15, 12, 19, 8, 11, 17, 5, 8, 5, 14, 13, 1, 17, 12, 4, 11, 8, 17, 10, 3, 16, 6, 3, 17, 8, 10, 13, 17, 2, 13, 19, 12, 10, 2, 7, 16, 3, 14, 1, 9, 10, 3, 4, 17, 13, 0, 3, 14, 14, 14, 19, 14, 13, 14, 5, 18, 3, 9, 11, 4, 16, 8, 2, 14, 11, 12, 7, 1, 6, 17, 12, 4, 2, 11, 16, 14, 6, 2, 13, 5, 5, 14, 0, 3, 4, 14, 15, 9, 3, 0, 10, 9, 1, 0, 4, 10, 1, 5, 17, 12, 1, 5, 3, 5, 10, 10, 18, 6, 8, 16, 4, 8, 6, 4, 7, 17, 16, 0, 3, 8, 2, 3, 18, 9, 16, 10, 1, 4, 15, 7, 4, 6, 7, 4, 9, 8, 14, 3, 3, 9, 18, 3, 6, 1, 15, 6, 12, 3, 3, 18, 12, 3, 7, 3, 6, 12, 12, 1, 0, 0, 8, 0, 2, 0, 10, 14, 10, 17, 16, 10, 19, 12, 5, 13, 2, 12, 14, 13, 16, 17, 2, 16, 15, 7, 8, 16, 10, 4, 3, 15, 2, 16, 5, 13, 10, 9, 4, 19, 4, 14, 0, 19, 14, 1, 19, 8, 10, 15, 6, 12, 17, 19, 7, 14, 1, 5, 9, 0, 17, 16, 7, 10, 14, 1, 2, 3, 11, 14, 10, 19, 6, 18, 2, 10, 18, 7, 1, 19, 12, 15, 0, 6, 10, 9, 15, 12, 17, 8, 3, 14, 7, 19, 18, 8, 8, 0, 3, 17, 12, 9, 17, 13, 12, 0, 3, 8, 17, 13, 6, 8, 16, 3, 5, 15, 4, 8, 3, 1, 4, 4, 10, 16, 2, 14, 16, 19, 15, 2, 0, 12, 7, 17, 14, 6, 1, 14, 11, 10, 5, 8, 3, 19, 12, 6, 15, 1, 6, 0, 3, 4, 2, 9, 5, 1, 9, 3, 10, 9, 15, 13, 17, 14, 10, 18, 2, 10, 12, 7, 12, 2, 19, 9, 17, 14, 3, 9, 13, 16, 3, 16, 0, 19, 19, 16, 14, 1, 17, 18, 16, 7, 18, 9, 15, 7, 15, 9, 7, 13, 19, 5, 14]


freq = {}
hash_times = {}  # {hash:[t1, t2], hash2:[t1,t2]}
window = []
window_size = cache_size * 8


def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    update_window(hash_no)  # windowing of the frequency
    calc_relative_freq(hash_no)  # frequency used for mec caching eviction
    update_hash_time(hash_no)  # time update for opr prediction
    check_cache(hash_no, url)


def calc_relative_freq(x):
    global freq

    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1


def update_hash_time(x):
    global hash_times

    if x in hash_times:
        if len(hash_times[x]) >= (8 * cache_size):
            del hash_times[x][0]
        hash_times[x].append(time.time())
    else:
        hash_times[x] = [time.time()]


def update_window(i):
    global freq
    global window

    if len(window) >= window_size:
        freq[window[0]] -= 1
        del window[0]
        window.append(i)
    else:
        window.append(i)


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

        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cache_time = get_time()
        ip = mec_me['ip']
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
    for i in mec_list:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py insert "{}" "{}" "{}" "{}"'.format(hash_no, path, cache_time,
                                                                                             host_ip)

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

        if mec_me['ip'] in h_list:
            time = get_time()
            cmd = "cat /home/mec/cache/{}.html".format(hash_no)
            os.system(cmd)
            print('-----------------------------------')
            print('Cache Hit from localhost')
            print('-----------------------------------')
            H += 1
            cur.execute(
                "update CacheTable set DateTime = '" + time + "' where Hash = '" + hash_no + "' and Host_ip = '"
                + mec_me['ip'] + "';")
            con.close()
        elif len(host_ip_list) == 1:
            fetch_from_mec(hash_no, host_ip_list[0][0])

        elif len(host_ip_list) > 1:
            max_band_ip = h_list[random.randint(0, len(h_list) - 1)]
            fetch_from_mec(hash_no, max_band_ip)

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def frequently_used(hash_no):
    host_ip = mec_me['ip']
    global freq
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Hash FROM CacheTable WHERE Host_ip ='" + host_ip + "'")
        host_ip_list = cur.fetchall()
        li = []  # gives a hash list in this format ['84yehi8w4hew', '939owu2wj38ewj']
        for i in range(len(host_ip_list)):
            li.append(host_ip_list[i - 1][0])
        fre_li = {}  # gives a dictionary of hash in cache and freq
        for i in li:
            fre_li[i] = freq[i]
        min_freq = min(fre_li, key=fre_li.get)  # returns hash with min frequency

        if fre_li[min_freq] > freq[hash_no]:
            return 'no'
        elif fre_li[min_freq] <= freq[hash_no]:
            a = []
            for i in fre_li:
                if fre_li[i] == fre_li[min_freq]:  # checks if 2 or more hash have the same min hash value
                    a.append(i)
            if len(a) == 1:  # if min frequency value is unique to only 1 hash
                delete_least_frequent_mec(min_freq, host_ip)
                delete_least_frequent_locally(min_freq, host_ip)
                return 'yes'
            else:  # if min frequency value is not unique to only 1 hash
                cur.execute("SELECT Hash, DateTime FROM CacheTable where Host_ip = '" + host_ip + "'")

                data = cur.fetchall()  # returns array that looks like [('123a11', '12:00'), ('111b2b', '11:11'), ('222b2b', '11:13')]

                dict_data = dict(data)
                b = {}
                for i in a:
                    b[i] = dict_data[i]
                min_time_hash = min(b, key=b.get)  # returns the hash wih the min frequency and min time
                delete_from_mec(b[min_time_hash], host_ip)
                delete_least_frequent_locally(min_time_hash, host_ip)
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
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py del "{}" "{}" '.format(hash_no, host_ip)

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


'''
def get_max_band():
    # M1 = '10.1.1.1'
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
'''


def _eval(coef, t):
    global eqn
    # print('\ncoef : ', coef)
    eqn = f = numpy.poly1d(coef)
    return f(t)


def predict(t_series, deg):
    x = numpy.arange(len(t_series))
    # print('\nx=',x)
    coef = list(numpy.polyfit(x, t_series, deg))
    return _eval(coef, len(t_series) + 1)


def pfit(t_series, deg, id):
    d_thread[id] = predict(t_series, deg)


def thread_job(t_hash):
    global d_thread

    d_thread = {}
    h1 = Thread(target=pfit, args=(hash_times[t_hash[0]], 3, t_hash[0]))
    h2 = Thread(target=pfit, args=(hash_times[t_hash[1]], 3, t_hash[1]))
    h3 = Thread(target=pfit, args=(hash_times[t_hash[2]], 3, t_hash[2]))
    h4 = Thread(target=pfit, args=(hash_times[t_hash[3]], 3, t_hash[3]))

    h1.start()
    h2.start()
    h3.start()
    h4.start()


def prepare_db():
    global re_use
    host_ip = mec_me['ip']
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + host_ip + "'")
        d = cur.fetchone()
        r = d[0]  # This value represents how many data entries for host_ip
        if r >= cache_size:
            cur.execute("SELECT Hash FROM CacheTable where Host_ip = '" + host_ip + "'")

            data = cur.fetchall()  # returns array that looks like [('qu3823uejwdu2u',), ('298w98eu2hws9e2u',), ('9qo83he29wiu',)]

            hashes = []

            for i in data:
                hashes.append(i[0])
            hash_time_series_dic = {}
            for t in hashes:
                hash_time_series_dic[t] = len(hash_times[t])
            min_list_len = min(hash_time_series_dic, key=hash_time_series_dic.get)
            if hash_time_series_dic[
                min_list_len] > 4:  # the minimum length of list > 4 is the condition #  for using polynomial of degree 3 for prediction
                thread_job(hashes)

                max_hash = max(d_thread, key=d_thread.get)
                delete_least_frequent_mec(max_hash, host_ip)
                cur.execute("DELETE FROM CacheTable WHERE Hash = '" + max_hash + "' AND Host_ip = '" + host_ip + "'")
                con.commit()
                con.close()
                cmd = 'rm /home/mec/cache/{}.html'.format(max_hash)
                os.system(cmd)
            else:
                min_time_dic = {}
                for v in hashes:
                    min_time_dic[v] = hash_times[v][-1]
                min_time_hash = min(min_time_dic, key=min_time_dic.get)
                delete_least_frequent_mec(min_time_hash, host_ip)
                cur.execute(
                    "DELETE FROM CacheTable WHERE Hash = '" + min_time_hash + "' AND Host_ip = '" + host_ip + "'")
                con.commit()
                con.close()
                cmd = 'rm /home/mec/cache/{}.html'.format(min_time_hash)
                os.system(cmd)
            re_use += 1

            # cur.execute("SELECT * FROM CacheTable")

    except sqlite3.Error as e:
        print('Error Encountered: {}'.format(e))


def delete_from_mec(min_time, host_ip):
    for i in mec_list:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py delete "{}" "{}" '.format(min_time, host_ip)

        stdin, stdout, stderr = c.exec_command(cmd)


def cache_performance():
    global H
    global M
    global MH
    global window_size
    global re_use
    p = int((H / request_no) * 100)
    q = int(((H + MH) / request_no) * 100)
    print('----------------------------------------------------------')
    print('                   Cache Performance')
    print('----------------------------------------------------------')
    print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, q))
    print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(H, M))
    print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(MH, H + MH))
    print('----------------------------------------------------------')
    print('         Total use of Replacement Algorithm = {}'.format(re_use))
    print('----------------------------------------------------------')
    cmd = f"echo 'p{cache_size}_local_hits = {H} \np{cache_size}_miss = {M} \np{cache_size}_mec_hit = {MH} \n" \
          f"p{cache_size}_total_hit = {H+MH}' >> /home/mec/cache_result.py"
    os.system(cmd)


def getting_ready():
    global mec_me  # {'hostname': <hostname>, 'ip': <ip>}

    my_ip = ip_address()

    cmd = ['cat /etc/hostname | cut -c 1-4']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    print('hostname = {}'.format(hostname))

    cmd = ['netstat -nr | head -n 3 | tail -n 1 | cut -d " " -f 10']
    router_ip = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    print('router_ip = {}'.format(router_ip))

    mec_me = {'hostname': hostname, 'ip': my_ip}

    cmd = "bash /home/mec/files_cache/hosts.sh {}/24 > /home/mec/temp/names.txt".format(router_ip)

    os.system(cmd)
    mec_set = {my_ip, router_ip}
    fr = open('/home/mec/temp/names.txt', 'r')

    ips = []
    f1 = fr.readlines()
    for i in f1:
        ips.append(i[0:-1])

    fr.close()

    available_host = set(ips) - mec_set

    for i in available_host:
        try:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(i, port, un, pw)
            cmd = ('echo "' + "'{}' : '{}'".format(hostname, my_ip) + '" >> /home/mec/temp/mec_list.txt')

            stdin, stdout, stderr = c.exec_command(cmd)
        except:
            print('connecting. . .')
            print('make sure ssh is running on all MEC')


def zipf_dist(length, maximum,
              zi):  # length = length of array, maximum = max number in array, zi = zipf parameter values > 1
    raw_list = numpy.random.zipf(zi, size=length)
    formated_list = [i % maximum for i in raw_list]
    count_dict = {i: formated_list.count(i) for i in set(formated_list)}
    print(f'Frequency count: {count_dict}')
    return formated_list


def run_me():
    global mec_list  # {'mec1': ip_address, 'mec3': 'ip_address'}
    global request_no

    os.system('clear')
    request_no = int(input('number of requests: '))
    server_ip = input('web server ip: ')
    n = int(input('number of web(html) contents: '))
    zipf_param = float(input("Zipf paramter [1.1 - 2], could be float: "))
    for i in range(1, n + 1):
        cmd = 'echo "{}/{}.html" >> /home/mec/temp/web_test.txt'.format(server_ip, i)
        os.system(cmd)
    os.system('clear')
    print("getting ready to start. . .")
    getting_ready()
    time.sleep(3)
    os.system('clear')
    g = Figlet(font='bubble')

    print(g.renderText('MEC CACHING PROJECT'))
    print(g.renderText('                      BY     EMEKA'))

    while True:
        print('\n')
        s = input('Enter any key to start and "stop" to exit: ')
        if s == 'stop':
            print('\nProgramme Terminated')
            print(freq)
            cache_performance()
            os.system('rm /home/mec/temp/*')
            break
        else:
            mec_str = ''
            tr = open('/home/mec/temp/mec_list.txt', 'r')
            tp = tr.readlines()
            for i in tp:
                mec_str += i[0:-1] + ','
            mec = '{' + mec_str[0:-1] + '}'
            mec_list = ast.literal_eval(mec)
            ref = zipf_dist(request_no, n, zipf_param)
            for v in ref:
                fr = open('/home/mec/temp/web_test.txt', 'r')

                t = fr.readlines()

                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(3)
            '''

            for v in ref:
                fr = open('/home/mec/temp/web_test.txt', 'r')

                t = fr.readlines()
                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(3)
            '''


def main():
    run_me()


if __name__ == "__main__":
    main()
