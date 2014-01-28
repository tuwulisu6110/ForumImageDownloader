import gevent
import gevent.queue
from gevent import monkey, Greenlet
monkey.patch_all()

import os
import os.path

import requests
from forum.eyny import eyny
from company.DownloadWorker import DownloadWorker

temp_dir = u'./temp/'
def createImageFolder(ImageTitle):
	ImageTitle = ImageTitle
	local_folder = os.path.join(temp_dir, ImageTitle)
	if not os.path.exists(local_folder):
		print u'creating {0} folder to store comic file...'.format(local_folder)
		os.makedirs(local_folder)

def ask_info():
	username = raw_input('username : ')
	password = raw_input('password : ')
	questionid = raw_input('question id : ')
	answer = raw_input('answer : ')
	return (username, password, questionid, answer)

def eynyBoss(url):
	try:
		eynyInstance = eyny()

		# if we have not login yet
		# this implies no cookie too.
		if not eynyInstance.is_login():
			username, password, questionid, answer = ask_info()
			# if login is failed, we will simply return an empty queue
			if not eynyInstance.login(username, password, questionid, answer):
				print u'login failed -> password or username is wrong?'
				return gevent.queue.Queue()

		Title, EynyJobQueue = eynyInstance.parse_hcomic(url)
		createImageFolder(Title)
		#return EynyJobQueue
		return gevent.queue.Queue()
	finally:
		eynyInstance.logout()


eynyJobQueue = eynyBoss(u"http://www06.eyny.com/thread-8561520-1-9FJC8P4V.html")

# create worker and start them
workers = []
for i in range(5):
	workers.append(DownloadWorker(i, eynyJobQueue))
for i in range(5):
	workers[i].start()

# block until all the worker has done their job
gevent.joinall(workers)


