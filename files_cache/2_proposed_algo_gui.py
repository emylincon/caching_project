# This is the Proposed algorithm for this research

import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
import psutil
import ping_code as pc
from threading import Thread
from matplotlib import pyplot as plt
from pyfiglet import Figlet
import subprocess as sp
import ast
import numpy


__author__ = 'Emmanuel'
# mec_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3']

cache_size = 4
H = 0
M = 0
MH = 0
re_use = 0
# ref = [1, 3, 5, 6, 4, 5, 1, 5, 5, 4, 0, 2, 0, 2, 0, 1, 4, 6, 6, 1, 0, 4, 2, 3, 1, 3, 6, 4, 3, 3]
# ref = [14, 14, 7, 0, 15, 15, 5, 18, 7, 14, 8, 17, 10, 14, 10, 16, 17, 12, 16, 0, 4, 10, 1, 12, 4, 5, 7, 6, 14, 19, 18, 7, 10, 19, 5, 13, 8, 14, 10, 16, 10, 0, 0, 13, 2, 4, 9, 17, 14, 10, 10, 5, 19, 11, 0, 16, 8, 10, 19, 8, 8, 18, 13, 16, 16, 10, 7, 11, 15, 6, 19, 7, 6, 1, 10, 15, 1, 14, 13, 4, 5, 5, 9, 2, 5, 6, 14, 15, 11, 15, 7, 0, 4, 7, 0, 12, 7, 10, 13, 6, 16, 7, 14, 17, 6, 0, 12, 11, 12, 15, 12, 16, 9, 7, 13, 12, 10, 11, 9, 4, 6, 2, 15, 15, 3, 7, 15, 19, 4, 7, 14, 14, 0, 12, 4, 13, 14, 6, 7, 16, 6, 4, 16, 3, 15, 15, 9, 1, 5, 7, 15, 17, 4, 1, 15, 17, 18, 17, 5, 0, 16, 11, 10, 14, 6, 18, 5, 4, 17, 1, 15, 4, 10, 19, 19, 2, 7, 4, 3, 8, 15, 1, 2, 9, 8, 10, 17, 1, 12, 3, 2, 11, 14, 19, 16, 19, 4, 6, 13, 12, 13, 12, 3, 10, 7, 13, 12, 12, 8, 3, 3, 4, 7, 5, 7, 2, 0, 16, 1, 2, 7, 12, 10, 8, 16, 3, 10, 17, 11, 8, 10, 1, 18, 10, 0, 11, 12, 18, 8, 13, 6, 19, 0, 12, 18, 10, 9, 8, 10, 4, 1, 10, 15, 16, 11, 12, 6, 0, 12, 14, 18, 7, 1, 12, 4, 19, 0, 17, 3, 17, 7, 15, 3, 14, 6, 12, 6, 12, 19, 0, 10, 17, 14, 5, 9, 17, 18, 14, 6, 19, 9, 12, 12, 7, 0, 6, 11, 1, 7, 15, 4, 9, 14, 18, 10, 5, 15, 18, 11, 7, 19, 4, 11, 13, 4, 12, 1, 5, 5, 7, 9, 4, 18, 14, 4, 11, 5, 13, 5, 4, 13, 15, 15, 0, 1, 1, 14, 14, 6, 18, 9, 14, 15, 1, 5, 3, 17, 6, 0, 8, 9, 13, 13, 1, 4, 7, 10, 0, 12, 16, 18, 3, 1, 1, 18, 6, 1, 10, 8, 13, 16, 6, 15, 8, 2, 1, 10, 4, 7, 11, 13, 7, 9, 12, 9, 11, 10, 8, 11, 0, 3, 3, 14, 8, 15, 1, 15, 11, 19, 15, 14, 13, 5, 1, 16, 3, 17, 18, 16, 15, 13, 0, 11, 6, 10, 18, 16, 18, 6, 7, 16, 13, 6, 2, 0, 6, 6, 2, 9, 4, 12, 9, 10, 11, 18, 6, 11, 19, 14, 9, 9, 5, 8, 6, 1, 6, 19, 15, 7, 1, 9, 5, 13, 6, 12, 13, 19, 8, 14, 9, 0, 13, 8, 7, 13, 11, 11, 12, 8, 9, 3, 12, 7, 1, 4, 8, 6, 5, 17, 7, 19, 4, 18, 16, 4, 9, 8, 9, 4, 6, 7, 19, 18, 4, 12, 13, 11, 4, 19, 6]
ref = [14, 14, 7, 15, 15, 15, 5, 18, 7, 14, 8, 7, 10, 14, 10, 16, 7, 16, 12, 0, 4, 10, 1, 12, 4, 5, 7, 6, 14, 7, 18, 7, 10, 19, 5, 13, 8, 14, 10, 16, 10, 0, 0, 13, 7, 4, 9, 17, 14, 10, 10, 5, 19, 11, 0, 16, 8, 10, 19, 8, 8, 18, 13, 16, 16, 10, 7, 11, 15, 6, 7, 7, 6, 1, 10, 15, 1, 14, 13, 4, 5, 5, 9, 2, 5, 6, 6, 15, 11, 15, 7, 0, 4, 7, 0, 12, 7, 10, 13, 6, 16, 7, 14, 17, 6, 0, 12, 11, 12, 15, 12, 16, 9, 7, 13, 12, 10, 11, 9, 4, 6, 2, 15, 15, 7, 7, 15, 19, 4, 7, 14, 14, 0, 12, 4, 13, 14, 6, 7, 16, 6, 4, 16, 6, 15, 15, 9, 1, 5, 7, 7, 17, 4, 1, 15, 17, 18, 17, 6, 0, 6, 11, 10, 14, 6, 18, 5, 4, 17, 1, 15, 4, 10, 19, 19, 2, 7, 4, 7, 8, 15, 1, 2, 9, 8, 10, 17, 6, 6, 3, 6, 11, 14, 19, 16, 19, 4, 6, 13, 12, 13, 12, 3, 10, 7, 13, 12, 12, 8, 7, 7, 4, 7, 5, 7, 2, 0, 16, 1, 2, 7, 12, 10, 8, 16, 3, 10, 17, 11, 8, 10, 1, 18, 10, 10, 11, 12, 18, 8, 13, 6, 19, 0, 12, 18, 10, 9, 8, 10, 4, 1, 10, 15, 16, 11, 12, 6, 0, 12, 14, 18, 7, 1, 12, 4, 19, 0, 17, 3, 17, 7, 15, 3, 14, 6, 12, 6, 12, 19, 0, 10, 17, 14, 5, 9, 17, 18, 14, 6, 19, 9, 12, 12, 7, 0, 6, 11, 1, 7, 15, 4, 9, 14, 18, 10, 5, 15, 18, 11, 7, 19, 4, 11, 13, 4, 12, 1, 5, 5, 7, 9, 4, 18, 14, 4, 11, 5, 13, 5, 4, 13, 15, 15, 0, 1, 1, 14, 14, 6, 6, 9, 14, 15, 15, 5, 3, 15, 6, 0, 8, 13, 13, 13, 1, 4, 7, 10, 0, 12, 16, 18, 3, 1, 1, 18, 6, 1, 10, 8, 13, 16, 6, 15, 8, 15, 1, 10, 4, 7, 11, 13, 7, 9, 12, 9, 11, 10, 8, 11, 0, 11, 3, 14, 8, 15, 1, 15, 11, 19, 15, 14, 13, 5, 1, 16, 3, 17, 18, 16, 15, 13, 0, 11, 6, 10, 18, 16, 18, 6, 7, 16, 13, 6, 2, 0, 6, 6, 6, 9, 4, 12, 9, 10, 11, 18, 6, 11, 19, 14, 9, 9, 5, 8, 6, 1, 6, 19, 15, 7, 1, 9, 5, 13, 6, 12, 13, 19, 8, 14, 9, 0, 13, 8, 7, 13, 11, 11, 12, 8, 9, 3, 12, 7, 1, 4, 8, 6, 5, 17, 7, 19, 4, 18, 16, 4, 9, 8, 9, 4, 6, 7, 19, 18, 4, 12, 13, 11, 4, 19, 6]


freq = {}
hash_times = {}
window = []
window_size = cache_size * 8

x_axis = []
y_axis = []


def make_hash_dic(host_ip, n):
    h_dic = {}   # {url: hash}
    kolour = ['r', 'g', 'c', 'k', 'b', 'm', 'y']
    col = {}
    for i in range(1, n+1):
        url = '{}/{}.html'.format(host_ip, i)
        hash_me = 'get {} HTTP/1.0'.format(url)
        y = str.encode(hash_me)
        ha = hashlib.md5(y)
        hash_no = ha.hexdigest()
        h_dic[url] = hash_no
        col[url] = kolour[i-1]
    return [h_dic, col]


def plot_performance():
    global H
    global M
    global MH
    global re_use

    fig5 = plt.figure('Cache Performance')

    fig5 = plt.clf()

    fig5 = plt.ion()
    name = ['Hits', 'Misses', 'Co-operative-Hits', 'Algo use']
    ypos = ([0, 1, 2, 3])
    values = [H, M, (H + MH), re_use]

    fig5 = plt.xticks(ypos, name)
    fig5 = plt.bar(ypos, values, align='center', color='m')
    fig5 = plt.title('Cache Performance')

    fig5 = plt.ylabel('values')

    fig5 = plt.pause(2)


def plot_graphs():
    host = server_ip
    prev_t = 0
    rtt = pc.verbose_ping(host)
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    plot_resource_util(rtt, delta)
#    plot_relative_frequency()
#    plot_changing_freq()
#    plot_local_cache_freq()
    plot_performance()
    plt.show()


def calculate_mov_avg(a1):
    ma1=[] # moving average list
    avg1=0 # movinf average pointwise
    count=0
    for i in range(len(a1)):
        count+=1
        avg1=((count-1)*avg1+a1[i])/count
        ma1.append(avg1) #cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def plot_resource_util(x, y):
    fig1 = plt.figure('Resource Utilization')

    fig1 = plt.clf()
    x_axis.append(x)
    y_axis.append(y)
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(calculate_mov_avg(x_axis), linewidth=5, label='RTT')
    fig1 = plt.plot(calculate_mov_avg(y_axis), linewidth=5, label='CPU')
    fig1 = plt.title('CPU and RTT Utilization over Time')
    fig1 = plt.ylabel('CPU and RTT')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)


def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    update_window(hash_no)       # windowing of the frequency
    calc_relative_freq(hash_no)  # frequency used for mec caching eviction
    update_hash_time(hash_no)    # time update for opr prediction
    check_cache(hash_no, url)


def calc_relative_freq(x):
    global freq

    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

    plot_graphs()


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
        cmd = 'python3 /home/mec/files_cache/db_manage.py insert "{}" "{}" "{}" "{}"'.format(hash_no, path, cache_time, host_ip)

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
            max_band_ip = h_list[random.randint(0, len(h_list)-1)]
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
        li = []    # gives a hash list in this format ['84yehi8w4hew', '939owu2wj38ewj']
        for i in range(len(host_ip_list)):
            li.append(host_ip_list[i - 1][0])
        fre_li = {}     # gives a dictionary of hash in cache and freq
        for i in li:
            fre_li[i] = freq[i]
        min_freq = min(fre_li, key=fre_li.get)    # returns hash with min frequency

        if fre_li[min_freq] > freq[hash_no]:
            return 'no'
        elif fre_li[min_freq] <= freq[hash_no]:
            a = []
            for i in fre_li:
                if fre_li[i] == fre_li[min_freq]:       # checks if 2 or more hash have the same min hash value
                    a.append(i)
            if len(a) == 1:                            # if min frequency value is unique to only 1 hash
                delete_least_frequent_mec(min_freq, host_ip)
                delete_least_frequent_locally(min_freq, host_ip)
                return 'yes'
            else:                                      # if min frequency value is not unique to only 1 hash
                cur.execute("SELECT Hash, DateTime FROM CacheTable where Host_ip = '" + host_ip + "'")

                data = cur.fetchall()  # returns array that looks like [('123a11', '12:00'), ('111b2b', '11:11'), ('222b2b', '11:13')]

                dict_data = dict(data)
                b = {}
                for i in a:
                    b[i] = dict_data[i]
                min_time_hash = min(b, key=b.get)         # returns the hash wih the min frequency and min time
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
    return _eval(coef, len(t_series)+1)


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
            if hash_time_series_dic[min_list_len] > 4:              # the minimum length of list > 4 is the condition #  for using polynomial of degree 3 for prediction
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
                cur.execute("DELETE FROM CacheTable WHERE Hash = '" + min_time_hash + "' AND Host_ip = '" + host_ip + "'")
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
    q = int(((H+MH) / request_no) * 100)
    print('----------------------------------------------------------')
    print('                   Cache Performance')
    print('----------------------------------------------------------')
    print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, q))
    print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(H, M))
    print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(MH, H + MH))
    print('----------------------------------------------------------')
    print('         Total use of Replacement Algorithm = {}'.format(re_use))
    print('----------------------------------------------------------')
    cmd = "echo 'p{}_local_hits = {} \np{}_miss = {} \np{}_mec_hit = {} \n" \
          "p{}_total_hit = {}' >> /home/mec/cache_result.py".format(cache_size, H, cache_size, M, cache_size, MH, cache_size, H+MH)
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


def run_me():
    global hash_dic
    global mec_list  # {'mec1': ip_address, 'mec3': 'ip_address'}
    global server_ip
    global request_no
    global colour

    os.system('clear')
    server_ip = input('web server ip: ')
    n = int(input('number of web(html) contents: '))
    request_no = int(input('number of requests: '))
    for i in range(1, n+1):
        cmd = 'echo "{}/{}.html" >> /home/mec/temp/web_test.txt'.format(server_ip, i)
        os.system(cmd)
    '''
    result = make_hash_dic(server_ip, n)
    hash_dic = result[0]
    colour = result[1]
    os.system('clear')
    '''

    print("getting ready to start. . .")
    time.sleep(5)
    getting_ready()
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
            cmd = "echo 'p{}_rtt = {} \np{}_cpu = {}' >> /home/mec/cache_result.py".format(cache_size, calculate_mov_avg(x_axis), cache_size, calculate_mov_avg(y_axis))
            os.system(cmd)
            break
        else:
            mec_str = ''
            tr = open('/home/mec/temp/mec_list.txt', 'r')
            tp = tr.readlines()
            for i in tp:
                mec_str += i[0:-1] + ','
            mec = '{' + mec_str[0:-1] + '}'
            mec_list = ast.literal_eval(mec)
            '''
            for i in range(30):
                fr = open('/home/mec/temp/web_test.txt', 'r')

                t = fr.readlines()

                v = random.randint(0, (len(t) - 1))
                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(3)
            '''

            for v in ref:
                fr = open('/home/mec/temp/web_test.txt', 'r')

                t = fr.readlines()
                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(1)


def main():
    run_me()


if __name__ == "__main__":
    main()
