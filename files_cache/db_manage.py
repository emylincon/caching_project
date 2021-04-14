import sys
import sqlite3
import subprocess as sp

cmd = ['find /home/mec/ -name "cache.db"']
database = str(sp.check_output(cmd, shell=True), 'utf-8').strip()
conn = sqlite3.connect(database)
 
 
def create():
    curr=conn.cursor()
    qstr = 'create table if not exists CacheTable (' \
                                        'Hash varchar(30), ' \
                                        'Path varchar(70), ' \
                                        'DateTime varchar(30), ' \
                                        'Host_ip varchar(20)' \
                                        ')'
    curr.execute(qstr)
    conn.commit()
    curr.close()
 
 
def insert(tuple):
    curr = conn.cursor()
    qstr = "insert into CacheTable values('{}','{}','{}','{}')".format(tuple[0], tuple[1], tuple[2], tuple[3])
    curr.execute(qstr)
    conn.commit()
    curr.close()
 
 
def delete_from_mec(tuple):
    curr = conn.cursor()
    qstr = "delete FROM CacheTable WHERE DateTime = '" + tuple[0] + "' and Host_ip = '" + tuple[1] + "'"
    curr.execute(qstr)
    conn.commit()
    curr.close()
 
 
def del_from_mec(tuple):
    curr = conn.cursor()
    qstr = "delete FROM CacheTable WHERE Hash = '" + tuple[0] + "' and Host_ip = '" + tuple[1] + "'"
    curr.execute(qstr)
    conn.commit()
    curr.close()
 
 
def main(argv):
    tuple = []
    if argv[1] == 'insert':
        for i in range(2, len(argv)):
            tuple.append(argv[i])
        insert(tuple)
    elif argv[1] == 'delete':
        for i in range(2, len(argv)):
            tuple.append(argv[i])
        delete_from_mec(tuple)
    elif argv[1] == 'del':
        for i in range(2, len(argv)):
            tuple.append(argv[i])
        del_from_mec(tuple)
    else:
        print('Wrong Keyword: {}'.format(argv[1]))
 
 
if __name__ == '__main__':
    main(sys.argv)
