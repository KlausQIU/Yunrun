# !usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import time
from datetime import date,datetime,timedelta
import os
from base import BACKUP_COUNT,BACKUP_PATH,BACKUP_DB

# 定时器
class Clock:
    def __init__(self):
        pass 

    def add_task(self,func,schedule_time,interval_time):
        schedule_times = self.schedule(schedule_time)
        interval_times = self.interval(interval_time)
        return self.run(func,schedule_times,interval_times)

    def run(self,func,schedule_times,interval_times):
        print 'perpare run %s'%(getattr(func,'__name__'))
        while True:
            if schedule_times:
                for schedule_time in schedule_times:
                    now = datetime.now()
                    str_time = now.strftime('%H:%M')
                    if schedule_time == str_time:
                        func()
                        print 'schedule time:'+now.strftime('%H:%M:%S')
            if interval_times:
                for interval_time in interval_times:
                    now = datetime.now()
                    str_time = now.strftime('%H:%M')
                    if interval_time == str_time:
                        func()
                        print 'interval_time:'+now.strftime('%H:%M:%S')
            time.sleep(2)
            continue

    def schedule(self,get_time):
        if get_time == '':
            run_times = []
        else:
        	run_times = get_time.split(',')
        return run_times

    def interval(self,get_time):
        interval_times = []
        if get_time == '':
            run_times = []
        else:
        	times = get_time.split(',')
        for t in times:
            interval_times.append('%s'%(t))
        return interval_times

# 备份
def backup_run():
    init_now = datetime.now()
    today = init_now.strftime('%Y%m%d%H%M')
    argv = {}
    db = BACKUP_DB
    path = BACKUP_PATH
    path += today
    argv['o'] = path
    argv['d'] = db
    mongodb_dump(**argv)
    delete_old(BACKUP_PATH)

def mongodb_dump(**kw):
	now = datetime.now()
	strnow = now.strftime('%H:%M')
	print "Backup time:",strnow
	dump = 'mongodump '
	for key in kw:
		argument1 = ' -%s'%key+' %s'%kw[key]
		dump += argument1
	if subprocess.call(dump,shell=True):
		print 'Backup done!'

def delete_old(path):
	count = 0
	for file in os.listdir(path):
		if(os.path.isdir(path+file)):
			count+=1
	if count > BACKUP_COUNT:
		delete_filename = sorted(os.listdir(path))[0]
		delete = 'rm -rf '
		delete += path
		delete += delete_filename
		subprocess.call(delete,shell=True)

# 其他
def other():
    pass

if __name__ == "__main__":
	clock = Clock()
	clock.add_task(backup_run,'09:53','52')
