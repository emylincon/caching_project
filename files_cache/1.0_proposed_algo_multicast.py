import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import time
import subprocess as sp
from threading import Thread
from pyfiglet import Figlet
import numpy as np
import struct
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import config
import smtplib
from email.message import EmailMessage
import random as r
import psutil
import pickle
import json
import re

__author__ = 'Emmanuel'

mec_list = {}  # {'mec1': ip_address, 'mec3': 'ip_address'}
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind to the server address
sock.bind(server_address)
# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


class Record:
    system = psutil.Process(os.getpid())

    def __init__(self, window_size, title):
        self.data_set = []
        self.window_size = window_size
        self.title = title
        self.count = 0

    def get_data(self):
        return 1

    def add_data(self):
        data = self.get_data()
        new_avg = self.calculate_mov_avg(data)
        self.check_window_size()
        self.data_set.append(new_avg)

    def check_window_size(self):
        if len(self.data_set) > self.window_size:
            outfile = open(f'results/{self.title}/{self.count}.pickle', 'wb')
            pickle.dump(self.data_set, outfile)
            outfile.close()
            self.data_set = self.data_set[-1:]
            self.count += 1

    def calculate_mov_avg(self, a1):
        _count = len(self.data_set)
        if _count == 0:
            avg1 = 0
        else:
            avg1 = self.data_set[-1]
        _count += 1
        avg1 = ((_count - 1) * avg1 + a1) / _count  # cumulative average formula μ_n=((n-1) μ_(n-1)  + x_n)/n
        return round(avg1, 4)


class CPU(Record):
    def get_data(self):
        cpu = psutil.cpu_percent(percpu=False)
        try:
            lst = self.data_set[-1]
        except IndexError:
            lst = psutil.cpu_percent(percpu=False)
        return round(abs(cpu - lst), 4)


class Memory(Record):

    def get_data(self):
        return round(self.system.memory_percent(), 4)


class Delay(Record):
    def __init__(self, window_size, title, server_ip):
        super().__init__(window_size, title)
        self.server_ip = server_ip

    def ping(self, host):
        cmd = [f'ping -c 1 {host}']
        try:
            output = str(sp.check_output(cmd, shell=True), 'utf-8').split('\n')
        except sp.CalledProcessError:
            print(f'{host} -> destination unreachable..')
            return self.data_set[-1]
        try:
            value = float(output[-2].split('=')[-1].split('/')[0])
        except ValueError:
            print(f"{output[-2].split('=')[-1].split('/')[0]} -> Ping Value Error")
            value = self.data_set[-1]
        return value

    def get_data(self):
        rtt = self.ping(self.server_ip)
        return round(rtt, 4)


class Algo:
    def __init__(self, cache_size, window_size, degree=3):
        self.cache_size = cache_size
        self.base_folder = '/home/mec/caching_project'
        self.cache_folder = f'{self.base_folder}/cache'
        self.hits = 0
        self.miss = 0
        self.collaborative_hits = 0
        self.freq = {}
        self.count = 0
        self.history = {}
        self.degree = degree
        self.window_size = window_size
        self.ssh_client = {'username': 'mec', 'password': 'password', 'port': 22}

    @staticmethod
    def request(page):
        return f'https://competent-euler-834b51.netlify.app/pages/{page}.html'

    def prepare_history(self, data):
        history = {}
        for j in set(data):
            history[self.get_hash(self.request(j))] = [i for i, x in enumerate(data) if x == j]
        self.history = history

    def hit_ratio(self):
        return round((((self.hits + self.collaborative_hits) / request_no) * 100), 4)

    def cache_performance(self) -> dict:
        p = int((self.hits / request_no) * 100)

        print('----------------------------------------------------------')
        print('                   Cache Performance')
        print('----------------------------------------------------------')
        print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, self.hit_ratio()))
        print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(self.hits, self.miss))
        print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(self.collaborative_hits,
                                                                           self.collaborative_hits + self.hits))
        print('----------------------------------------------------------')

        cache_details = {'hits': self.hits, 'miss': self.miss, 'mec_hit': self.collaborative_hits,
                         'total_hit_ratio': self.hit_ratio(),
                         'collaborative_ratio': round((self.collaborative_hits / (self.collaborative_hits + self.hits)),
                                                      4)}
        return cache_details

    def push(self, page_no):
        url = self.request(page_no)
        hash_no = self.get_hash(url=url)
        self.calc_relative_freq(hash_no)  # frequency used for mec caching eviction
        self.maintain_history(hash_no)  # time update for opr prediction
        self.check_cache(hash_no, url)

    def calc_relative_freq(self, cache):
        if cache in self.freq:
            self.freq[cache] += 1
        else:
            self.freq[cache] = 1

    @staticmethod
    def get_hash(url):
        hash_me = 'get {} HTTP/1.0'.format(url)
        y = str.encode(hash_me)
        ha = hashlib.md5(y)
        return ha.hexdigest()

    def maintain_history(self, cache):
        self.count += 1
        if cache in self.history:
            if len(self.history[cache]) > self.window_size:
                self.history[cache].pop(0)
            self.history[cache].append(self.count)
        else:
            self.history[cache] = [self.count]

    def check_cache(self, hash_no, url):
        result = Database().select_hash_count(hash_no)[0]  # is cache in cache_store
        if result == 0:
            self.fetch_from_source(hash_no, url)
        else:
            self.fetch_from_cache(hash_no)

    def fetch_from_source(self, hash_no, url):
        cmd = "curl {}".format(url)
        os.system(cmd)

        self.maintain_cache_size()  # CHECKS IF CACHE IS FULL AND ELIMINATES VICTIM

        cmd = "echo `curl {}` > {}/{}.html".format(url, self.cache_folder, hash_no)  # CACHES DATA FROM SOURCE
        os.system(cmd)
        print('-----------------------------------')
        print('Cache Miss')
        print('-----------------------------------')
        self.miss += 1
        result = Database().update_local_database(hash_no)
        Database().update_mec_database(*result)

    @staticmethod
    def lfu(cache_dict):
        return min(cache_dict, key=cache_dict.get)

    @staticmethod
    def lru(cache_dict):
        victim = min(cache_dict.keys(), key=(lambda k: cache_dict[k][-1]))
        print(f"Replaced using LRU -> victim -> {victim}")
        return victim

    def evict_hash(self, host_ip, hash_no, hash_time=None):
        self.delete_least_frequent_mec(hash_no, host_ip)
        if hash_time is None:
            Database().delete_row_with_hash(host_ip=host_ip, hash_no=hash_no)
        else:
            Database().delete_row_with_time(host_ip=host_ip, hash_time=hash_time)
        cmd = 'rm {}/{}.html'.format(self.cache_folder, hash_no)
        os.system(cmd)

    def maintain_cache_size(self):  # cache_full? replace and update
        host_ip = mec_me['ip']
        data = Database().select_hash_from_host(host_ip)
        if len(data) >= self.cache_size:
            cache_dict = {pod[0]: self.history[pod[0]] for pod in data}
            min_key = min(cache_dict.keys(), key=(lambda k: len(cache_dict[k])))
            min_len = len(cache_dict[min_key])
            # the minimum length of list > 4 is the condition #  for using polynomial of degree 3 for prediction
            if min_len > self.degree + 1:
                max_hash = OPR(degree=self.degree, cache_dict=cache_dict).find_victim()
                self.evict_hash(hash_no=max_hash, host_ip=host_ip)
            else:
                min_time_hash = self.lru(cache_dict=cache_dict)
                self.evict_hash(host_ip=host_ip, hash_no=min_time_hash)

    def fetch_from_cache(self, hash_no):
        hosts = Database().select_host_ip_with_hash(hash_no)
        h_list = [i[0] for i in hosts]
        if mec_me['ip'] in h_list:
            self.fetch_locally(hash_no)
            self.hits += 1

        elif len(h_list) == 1:
            self.fetch_from_mec(hash_no, h_list[0])
            self.collaborative_hits += 1

        elif len(h_list) > 1:
            host = self.min_delay(h_list)
            self.fetch_from_mec(hash_no, host)
            self.collaborative_hits += 1

    @staticmethod
    def min_delay(hosts: list) -> str:
        d_dict = {mec: delay.ping(mec) for mec in hosts}
        return min(d_dict, key=d_dict.get)

    def fetch_locally(self, hash_no):
        t_time = get_time()
        cmd = "cat {}/{}.html".format(self.cache_folder, hash_no)
        os.system(cmd)
        print('-----------------------------------')
        print('Cache Hit from localhost')
        print('-----------------------------------')

        Database().update_access_time(hash_no=hash_no, hash_time=t_time)

    def fetch_from_mec(self, hash_no, host_ip):
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host_ip, self.ssh_client['port'], self.ssh_client['username'], self.ssh_client['password'])
        cmd = 'cat {}/{}.html'.format(self.cache_folder, hash_no)

        stdin, stdout, stderr = c.exec_command(cmd)

        ip = ip_address()

        c_size = len(
            Database().select_hash_from_host(host_ip=ip))  # This value represents how many data entries for host_ip

        if c_size >= self.cache_size and self.frequently_used(hash_no) == 'no':
            for line in stdout:
                q = len(line) - 1
                t = line[:q]
                print(t)
            print('-----------------------------------')
            print('Hit from MEC Not Cached')
            print('-----------------------------------')

        else:
            for line in stdout:
                q = len(line) - 1
                t = line[:q]
                cmd = "echo '{}' >> {}/{}.html".format(t, self.cache_folder, hash_no)
                os.system(cmd)
            cmd = 'cat {}/{}.html'.format(self.cache_folder, hash_no)
            result = Database().update_local_database(hash_no)
            Database().update_mec_database(*result)
            os.system(cmd)
            print('-----------------------------------')
            print('Cache Hit from MEC')
            print('-----------------------------------')

    def frequently_used(self, hash_no):
        host_ip = mec_me['ip']

        host_ip_list = Database().select_hash_from_host(host_ip=host_ip)  # [('13r2fcerf3f',), ('1ed2d32c2d2x',)]

        fre_li = {pod[0]: self.freq[pod[0]] for pod in host_ip_list}
        min_freq = self.lfu(fre_li)  # returns hash with min frequency

        if fre_li[min_freq] > self.freq[hash_no]:
            return 'no'
        elif fre_li[min_freq] <= self.freq[hash_no]:
            # checks if 2 or more hash have the same min hash value
            a = [i for i in fre_li if fre_li[i] == fre_li[min_freq]]
            if len(a) == 1:  # if min frequency value is unique to only 1 hash
                self.evict_hash(hash_no=min_freq, host_ip=host_ip)
                return 'yes'
            else:  # if min frequency value is not unique to only 1
                s = tuple(a)
                # returns array that looks like [('123a11', '12:00'), ('111b2b', '11:11'), ('222b2b', '11:13')]
                data = Database().select_hash_datetime(host_ip=host_ip, hashes=s)
                b = dict(data)
                min_time_hash = min(b, key=b.get)  # returns the hash wih the min frequency and min time
                self.evict_hash(host_ip=host_ip, hash_no=min_time_hash)
                return 'yes'

    def delete_least_frequent_mec(self, hash_no, host_ip):
        for i in mec_list:
            c = paramiko.SSHClient()

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(mec_list[i], self.ssh_client['port'], self.ssh_client['username'], self.ssh_client['password'])
            cmd = 'python3 {}/files_cache/db_manage.py del "{}" "{}" '.format(self.base_folder, hash_no, host_ip)

            stdin, stdout, stderr = c.exec_command(cmd)


class OPR:
    def __init__(self, degree, cache_dict):
        self.degree = degree
        self.cache_dict = cache_dict

    def predict(self, data):
        feature = np.array(data[:-1])
        target = np.array(data[1:])

        poly_reg = PolynomialFeatures(degree=self.degree)
        feature_poly = poly_reg.fit_transform(feature.reshape(-1, 1))
        to_predict = poly_reg.fit_transform(target[-1:].reshape(-1, 1))

        lin_reg = LinearRegression()
        lin_reg.fit(feature_poly, target.reshape(-1, 1))
        my_pred = lin_reg.predict(feature_poly)
        print('Prediction score => ', r2_score(target, my_pred))
        return lin_reg.predict(to_predict)[0][0]

    def find_victim(self):
        predicted = {cache: self.predict(self.cache_dict[cache]) for cache in self.cache_dict}
        victim = max(predicted.keys(), key=(lambda k: predicted[k]))
        return victim


class Database:
    def __init__(self):
        self.base_folder = '/home/mec/caching_project'
        self.cache_folder = f'{self.base_folder}/cache'
        self.con = sqlite3.connect(f'{self.base_folder}/cache.db')
        self.cur = self.con.cursor()

    def select_hash_count(self, hash_no):
        self.cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Hash='" + hash_no + "'")
        result = self.cur.fetchone()
        self.con.close()
        return result

    def select_hash_from_host(self, host_ip):
        self.cur.execute("SELECT Hash FROM CacheTable where Host_ip = '" + host_ip + "'")

        data = self.cur.fetchall()
        self.con.close()
        # returns array that looks like [('qu3823uejwdu2u',), ('298w98eu2hws9e2u',), ('9qo83he29wiu',)]
        return data

    def select_host_ip_with_hash(self, hash_no):
        self.cur.execute("SELECT Host_ip FROM CacheTable WHERE Hash='" + hash_no + "'")
        host_ip_list = self.cur.fetchall()
        self.con.close()
        return host_ip_list

    def select_hash_datetime(self, host_ip, hashes):
        self.cur.execute(
            "SELECT Hash, DateTime FROM CacheTable where Host_ip = '" + host_ip + f"' AND Hash in {hashes}")

        data = self.cur.fetchall()
        self.con.close()
        return data

    def update_access_time(self, hash_no, hash_time):
        self.cur.execute(
            "update CacheTable set DateTime = '" + hash_time + "' where Hash = '" + hash_no + "' and Host_ip = '"
            + mec_me['ip'] + "';")
        self.con.close()

    def delete_row_with_hash(self, hash_no, host_ip):
        self.cur.execute("DELETE FROM CacheTable WHERE Hash = '" + hash_no + "' AND Host_ip = '" + host_ip + "'")
        self.con.commit()
        self.con.close()

    def delete_row_with_time(self, hash_time, host_ip):
        self.cur.execute(
            "DELETE FROM CacheTable WHERE Hash = '" + hash_time + "' AND Host_ip = '" + host_ip + "'")
        self.con.commit()
        self.con.close()

    def update_local_database(self, hash_no):
        try:
            cache_time = get_time()
            ip = mec_me['ip']
            path = '{}/{}.html'.format(self.cache_folder, hash_no)
            data = (hash_no, path, cache_time, ip)
            self.cur.execute("INSERT INTO CacheTable VALUES(?, ?, ?, ?)", data)
            self.con.commit()
            self.cur.execute("SELECT * FROM CacheTable")
            d = self.cur.fetchall()

            for row in d:
                print(row)
            result = (hash_no, path, cache_time, ip)
            self.con.close()
            return result

        except sqlite3.Error as e:
            print('Error in cache_update: {}'.format(e))
            self.con.close()

    def update_mec_database(self, hash_no, path, cache_time, host_ip):
        for i in mec_list:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(mec_list[i], port, un, pw)
            cmd = 'python3 {}/files_cache/db_manage.py insert "{}" "{}" "{}" "{}"'.format(self.base_folder, hash_no,
                                                                                          path,
                                                                                          cache_time,
                                                                                          host_ip)
            stdin, stdout, stderr = c.exec_command(cmd)


def get_time():
    y = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return y


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def send_message(mg):
    _multicast_group = ('224.3.29.71', 10000)
    try:

        # Send data to the multicast group
        if mg == 'hello':
            smg = mg + ' ' + get_hostname()
            sock.sendto(str.encode(smg), _multicast_group)
            print('\nHello message sent')

    except Exception as e:
        print(e)


def get_hostname():
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8').strip()
    return hostname


def receive_message():
    while True:
        if len(mec_list) == mec_no:
            # print('MEC Details: ', mec_list)
            del mec_list[get_hostname()]
            break
        data, address = sock.recvfrom(1024)

        if data.decode()[:5] == 'hello':
            mec_list[data.decode()[6:]] = address[0]


def initialization():
    global mec_no
    global mec_me  # {'hostname': <hostname>, 'ip': <ip>}

    hostname = get_hostname()
    print('hostname = {}'.format(hostname))

    mec_me = {'hostname': hostname, 'ip': ip_address()}

    try:
        mec_no = int(input('Number of MECs: ').strip())
        print('\nCompiling MEC Details')
        h1 = Thread(target=receive_message)
        h1.start()
        while True:
            b = input('Send Hello Message (Y/N): ').strip().lower()
            if b == 'y':
                send_message('hello')
                break
            else:
                print('\nPlease Type "y" to send Hello message\n')
    except KeyboardInterrupt:
        print('\nProgramme Terminated')
        exit(0)


def zipf_dist(length, maximum):  # length = length of array, maximum = max number in array
    raw_list = np.random.zipf(1.35, size=length)
    formated_list = [i % maximum for i in raw_list]
    count_dict = {i: formated_list.count(i) for i in set(formated_list)}
    print(f'Frequency count: {count_dict}')
    return formated_list


class DataObj:
    def __init__(self, server_ip):
        self.email = config.email_address
        self.password = config.password
        self.email_receiver = config.send_email
        self.result_server_ip = server_ip

    def send_email(self, msg):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com')
            server.ehlo()
            server.login(self.email, self.password)
            subject = 'Caching results {} {}'.format('Proposed caching', get_hostname())
            # msg = 'Attendance done for {}'.format(_timer)
            _message = 'Subject: {}\n\n{}\n\n SENT BY RIHANNA \n\n'.format(subject, msg)
            server.sendmail(self.email, self.email_receiver, _message)
            server.quit()
            print("Email sent!")
        except Exception as e:
            print(e)

    def send_email_attachment(self, file):
        msg = EmailMessage()

        msg['Subject'] = 'Caching results {} {}'.format('Proposed caching', get_hostname())

        msg['From'] = self.email

        msg['To'] = self.email_receiver
        msg.set_content(file)
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email, self.password)
            smtp.send_message(msg)

    def save_data(self, mem, cpu, my_delay, no, cache_details):
        host = get_hostname()
        host_no = int(re.findall('[0-9]+', host)[0])
        data = f"""
        memory{host_no}_{no} = {mem}
        cpu{host_no}_{no} = {cpu}
        delay{host_no}_{no} = {my_delay}
        """
        detail = '\n'
        for det in cache_details:
            detail += f'{det}{host_no}_{no} = {cache_details[det]}\n'
        data += detail
        self.send_email(data)
        file = open(f'results/output{host_no}_{no}.py', 'w')
        file.write(data)
        file.close()
        send_path = '/home/osboxes/results/'
        sp.run(
            ["scp", f'results/output{host_no}_{no}.py', f"osboxes@{self.result_server_ip}:{send_path}"])
        for res in ['MEM', 'CPU', 'RTT']:
            os.system(f'zip results/{res}{host_no}_{no}.zip results/{res}/*')
            sp.run(
                ["scp", f'results/{res}{host_no}_{no}.zip', f"osboxes@{self.result_server_ip}:{send_path}"])
            self.send_email_attachment(f'results/{res}{host_no}_{no}.zip')
            time.sleep(r.uniform(1, 10))


def data_slice(no_mec, total_req_no, initial):
    host = get_hostname()
    host_no = int(re.findall('[0-9]+', host)[0])
    step = int(total_req_no / no_mec)
    start = host_no * step
    return start + initial, start + step + initial


def run_me():
    global mec_list  # {'mec1': ip_address, 'mec3': 'ip_address'}
    global request_no, delay

    os.system('clear')
    # total_request_no = int(input('Total number of requests: '))
    total_request_no = 10_002
    server_ip = 'competent-euler-834b51.netlify.app'
    # server_ip = input('web server ip: ')
    result_server = input('Result server ip: ')
    os.system('clear')
    print("getting ready to start. . .")
    initialization()
    time.sleep(2)
    os.system('clear')
    g = Figlet(font='bubble')

    print(g.renderText('MEC CACHING PROJECT'))
    print(g.renderText('                      BY     EMEKA'))
    cache_store = Algo(cache_size=30, window_size=800)
    delay = Delay(window_size=200, title='RTT', server_ip=server_ip)
    cpu = CPU(window_size=200, title='CPU')
    mem = Memory(window_size=200, title='MEM')

    input('\nEnter any key to start: ')
    with open('dataset.json') as json_file:
        data = json.load(json_file)
    start, stop = data_slice(no_mec=mec_no, total_req_no=total_request_no,
                             initial=len(data['requests'])-total_request_no)
    hist, ref = data['requests'][:start], data['requests'][start:stop]
    request_no = stop-start
    cache_store.count = request_no - 1
    cache_store.prepare_history(hist)
    for ind in range(len(ref)):
        page_no = ref[ind]
        print(f'\nRequesting ({ind}/{request_no})\n')
        cache_store.push(page_no)
        cpu.add_data()
        mem.add_data()
        delay.add_data()
        time.sleep(2)
    cache_details = cache_store.cache_performance()
    DataObj(server_ip=result_server).save_data(mem=mem.data_set, cpu=cpu.data_set, my_delay=delay.data_set, no=mec_no,
                                               cache_details=cache_details)
    print('Experiment Concluded!')


def main():
    run_me()


if __name__ == "__main__":
    main()
