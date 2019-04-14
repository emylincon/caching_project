
# This is an LRU and cooperative caching algorithm with real-time graphical results

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
import subprocess as sp
import ast
from matplotlib import pyplot as plt
from pyfiglet import Figlet


__author__ = 'Emmanuel'
# mec_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3']

cache_size = 4
H = 0
M = 0
MH = 0
re_use = 0
x_axis = []
y_axis = []
requests = []
# ref = [5, 0, 5, 3, 6, 0, 4, 1, 3, 5, 5, 6, 0, 5, 5, 2, 6, 5, 2, 6, 4, 1, 4, 4, 5, 6, 0, 3, 2, 6]
ref = [14, 14, 7, 15, 15, 15, 5, 18, 7, 14, 8, 7, 10, 14, 10, 16, 7, 16, 12, 0, 4, 10, 1, 12, 4, 5, 7, 6, 14, 7, 18, 7, 10, 19, 5, 13, 8, 14, 10, 16, 10, 0, 0, 13, 7, 4, 9, 17, 14, 10, 10, 5, 19, 11, 0, 16, 8, 10, 19, 8, 8, 18, 13, 16, 16, 10, 7, 11, 15, 6, 7, 7, 6, 1, 10, 15, 1, 14, 13, 4, 5, 5, 9, 2, 5, 6, 6, 15, 11, 15, 7, 0, 4, 7, 0, 12, 7, 10, 13, 6, 16, 7, 14, 17, 6, 0, 12, 11, 12, 15, 12, 16, 9, 7, 13, 12, 10, 11, 9, 4, 6, 2, 15, 15, 7, 7, 15, 19, 4, 7, 14, 14, 0, 12, 4, 13, 14, 6, 7, 16, 6, 4, 16, 6, 15, 15, 9, 1, 5, 7, 7, 17, 4, 1, 15, 17, 18, 17, 6, 0, 6, 11, 10, 14, 6, 18, 5, 4, 17, 1, 15, 4, 10, 19, 19, 2, 7, 4, 7, 8, 15, 1, 2, 9, 8, 10, 17, 6, 6, 3, 6, 11, 14, 19, 16, 19, 4, 6, 13, 12, 13, 12, 3, 10, 7, 13, 12, 12, 8, 7, 7, 4, 7, 5, 7, 2, 0, 16, 1, 2, 7, 12, 10, 8, 16, 3, 10, 17, 11, 8, 10, 1, 18, 10, 10, 11, 12, 18, 8, 13, 6, 19, 0, 12, 18, 10, 9, 8, 10, 4, 1, 10, 15, 16, 11, 12, 6, 0, 12, 14, 18, 7, 1, 12, 4, 19, 0, 17, 3, 17, 7, 15, 3, 14, 6, 12, 6, 12, 19, 0, 10, 17, 14, 5, 9, 17, 18, 14, 6, 19, 9, 12, 12, 7, 0, 6, 11, 1, 7, 15, 4, 9, 14, 18, 10, 5, 15, 18, 11, 7, 19, 4, 11, 13, 4, 12, 1, 5, 5, 7, 9, 4, 18, 14, 4, 11, 5, 13, 5, 4, 13, 15, 15, 0, 1, 1, 14, 14, 6, 6, 9, 14, 15, 15, 5, 3, 15, 6, 0, 8, 13, 13, 13, 1, 4, 7, 10, 0, 12, 16, 18, 3, 1, 1, 18, 6, 1, 10, 8, 13, 16, 6, 15, 8, 15, 1, 10, 4, 7, 11, 13, 7, 9, 12, 9, 11, 10, 8, 11, 0, 11, 3, 14, 8, 15, 1, 15, 11, 19, 15, 14, 13, 5, 1, 16, 3, 17, 18, 16, 15, 13, 0, 11, 6, 10, 18, 16, 18, 6, 7, 16, 13, 6, 2, 0, 6, 6, 6, 9, 4, 12, 9, 10, 11, 18, 6, 11, 19, 14, 9, 9, 5, 8, 6, 1, 6, 19, 15, 7, 1, 9, 5, 13, 6, 12, 13, 19, 8, 14, 9, 0, 13, 8, 7, 13, 11, 11, 12, 8, 9, 3, 12, 7, 1, 4, 8, 6, 5, 17, 7, 19, 4, 18, 16, 4, 9, 8, 9, 4, 6, 7, 19, 18, 4, 12, 13, 11, 4, 19, 6]


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


def plot_graphs():
    host = server_ip
    prev_t = 0
    rtt = pc.verbose_ping(host)
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    plot_resource_util(rtt, delta)
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

    # plt.show()


def plot_performance():
    global H
    global M
    global MH
    global re_use

    fig2 = plt.figure('Cache Performance')

    fig2 = plt.clf()

    fig2 = plt.ion()
    name = ['Hits', 'Misses', 'Co-operative-Hits', 'Algo use']
    ypos = ([0, 1, 2, 3])
    values = [H, M, (H + MH), re_use]

    fig2 = plt.xticks(ypos, name)
    fig2 = plt.bar(ypos, values, align='center', color='m')
    fig2 = plt.title('Cache Performance')

    fig2 = plt.ylabel('values')

    fig2 = plt.pause(2)


def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    check_cache(hash_no, url)
    plot_graphs()


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
        con = sqlite3.connect('/home/mec/cache.db')
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
            max_band_ip = h_list[random.randint(0, len(h_list)-1)]
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


'''
def get_max_band():
    M1 = '10.1.1.1'
    M2 = '10.2.2.2'
    #M3 = '10.3.3.3'
    conn = sqlite3.connect('/home/mec/cache.db')
    curr = conn.cursor()
    sql_cmd = "SELECT M1, M2 FROM Bw_Table ORDER BY Id DESC LIMIT 1;"
    curr.execute(sql_cmd)
    data = curr.fetchone()
    a = data[0]
    b = data[1]
    c = [a, b]
    d = max(c)
    e = c.index(d)
    if e == 0:
        return M1
    elif e == 1:
        return M2
'''


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
    cmd = f"echo 'lru{cache_size}_local_hits = {H} \nlru{cache_size}_miss = {M} \nlru{cache_size}_mec_hit = {MH} \n" \
          f"lru{cache_size}_total_hit = {H+MH}' >> /home/mec/cache_result.py"
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
            cache_performance()
            os.system('rm /home/mec/temp/*')
            cmd = f"echo 'lru{cache_size}_rtt = {calculate_mov_avg(x_axis)} \nlru{cache_size}_cpu = {calculate_mov_avg(y_axis)}' >> /home/mec/cache_result.py"
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
