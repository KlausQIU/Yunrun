# !usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import pymongo
import sys 
import time 
from datetime import date,datetime,timedelta
import os  

MONGODB_HOST = "localhost"
MONGODB_DB = "devplatform"
MONGODB_PORT = 27017
backup_count = 0


def mongodb_dump(**kw):
	dump = 'mongodump '
	for key in kw:
		argument1 = ' -%s'%key+' %s'%kw[key]
		dump += argument1
	subprocess.call(dump,shell=True)
		
def argument(db,path):
	init_now = datetime.now()
	today = init_now.strftime('%Y%m%d%H%M')
	argv = {}
	db = db
	path += db
	path += today
	argv['o'] = path
	argv['d'] = db
	return argv

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

def run_backup(func, day=0, hour=0, min=0, second=0):
	global backup_count
	now = datetime.now()
	strnow = now.strftime('%Y-%m-%d %H:%M:%S')
	print "now:",strnow
	period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
	next_time = now + period
	strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
	print "next run:",strnext_time
	while True:
		iter_now = datetime.now()
		iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
		if str(iter_now_time) == str(strnext_time):
			print "start work: %s" % iter_now_time
			db = 'devplatform'
			path = "/home/qiu1/dump/"
			argv = argument(db,path)
			if argv:
				func(**argv)
				backup_count += 1
			print "backup count:%s"%backup_count
			print "backup done."
			iter_time = iter_now + period
			strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
			print "next run: %s" % strnext_time
			delete_old(path)
			continue

if __name__ == "__main__":
	run_backup(mongodb_dump,second=10)
