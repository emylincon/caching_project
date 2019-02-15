import subprocess as sp
import sqlite3
 
 
ip1 = '10.2.2.2'
ip2 = '10.3.3.3'
 
 
def metric_convert(b_str):
 
    c = b_str[-9:]
    print('c is {}'.format(c))
    d = b_str[:-10]
    print('d is {}'.format(d))
 
    if c[0] == 'M':
        bw = float(d) * 1000
    else:
        bw = float(d)
 
    return bw
 
 
def fetch_bw_list(ip):
    try:
        print('fetching bw from {}'.format(ip))
        cmd = ['sh get_bw.sh {}'.format(ip)]
        x = str(sp.check_output(cmd, shell=True), 'utf-8')
        d1 = x[:(len(x) - 1)]
        d1_kbits = metric_convert(d1)
        return d1_kbits
 
    except Exception as e:
        print('Error in fetch bw: {}'.format(e))
 
 
def bandwidth_data():
    print('Running. . .')
    try:
        global id
        while True:
 
            conn = sqlite3.connect('/home/mec/cache.db')
            curr = conn.cursor()
            print('fetching count...')
            sql_cmd = "select count(*) from Bw_Table"
            curr.execute(sql_cmd)
            count = curr.fetchone()
            print('done')
            print('checking limit...')
            if count[0] >= 30:
                sql_cmd_1 = "delete from Bw_Table where Id in (select Id from Bw_Table limit 10)"
                curr.execute(sql_cmd_1)
            print('done')
 
            dd1 = fetch_bw_list(ip1)
            print('dd1 is {}'.format(dd1))
 
            dd2 = fetch_bw_list(ip2)
            print('dd2 is {}'.format(dd2))
 
            print('uploading data to database. . .')
            bw_values = "insert into Bw_Table(M2, M3) values('{}', '{}')".format(dd1, dd2)
            print(bw_values)
 
            curr.execute(bw_values)
            conn.commit()
            sql_cmd1 = "select * from Bw_Table"
            count1 = curr.execute(sql_cmd1)
            for line in count1:
                print(line)
            curr.close()
            print('done')
 
    except KeyboardInterrupt:
        print('\nProgramme Terminated')
 
 
def main():
    bandwidth_data()
 
 
if __name__ == '__main__':
    main()
