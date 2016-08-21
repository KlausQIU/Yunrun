# !/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import datetime
import time

#定时器
class Clock:
    def __init__(self):
        pass

    def add_task(self,func,run_time,interval_time):
        return self.run(func,run_time)

    def run(self,func,run_time):
        while True:
            self.run_time = '21'
            str_time = '21'
            if self.run_time == str_time:
                func()
            time.sleep(2)
            continue

def schedule_time(get_time):
    
#备份
def backup_run():
    init_now = datetime.now()
    today = init_now.strftime('%Y%m%d%H%M')
    argv = {}
    db = db
    path += today
    argv['o'] = path
    argv['d'] = db
    dump = 'mongodump '
    for key in argv:
        argument1 = ' -%s'%key+' %s'%kw[key]
        dump += argument1
    if subprocess.call(dump,shell=True):
        print 'backup Done!'
        delete_old(path)

def delete_old(path):
    count = 0
    for file in os.listdir(path):
        if(os.path.isdir(path+file)):
            count+=1
    if count >= 3:
        delete_filename = sorted(os.listdir(path))[0]
        delete = 'rm -rf '
        delete += path
        delete += delete_filename
        subprocess.call(delete,shell=True)


def draft():
    print 'hello'

if __name__ == '__main__':
    clock = Clock()
    clock.add_task(draft,'04:00','21')



