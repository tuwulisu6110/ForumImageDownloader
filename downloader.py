import gevent
import gevent.queue
from gevent import monkey, Greenlet
monkey.patch_all()

import os
import os.path

import requests
from forum.eyny import eyny
from company.DownloadWorker import DownloadWorker


# contains the DownloadJob
download_links = gevent.queue.Queue()

temp_dir = u'./temp/'
def createImageFolder(ImageTitle):
	ImageTitle = ImageTitle.replace(u'/', u'-')
	local_folder = os.path.join(temp_dir, ImageTitle)
	if not os.path.exists(local_folder):
		print u'creating {0} folder to store comic file...'.format(local_folder)
		os.makedirs(local_folder)


def eynyBoss():
	eynyInstance = eyny()
	username = raw_input('username : ')
	password = raw_input('password : ')
	questionid = raw_input('question id : ')
	answer = raw_input('answer : ')
	try:
		eynyInstance.login(username, password, questionid=questionid, answer=answer)
		Title, EynyJobQueue = eynyInstance.parsing(u"http://www09.eyny.com/thread-9361883-1-1.html")
		createImageFolder(Title)
		return EynyJobQueue
			
	finally:
		eynyInstance.logout()
def debug():
	for i in range(5):
		job = dict()
		job['comicTitle'] = u'hello'
		job['page'] = i
		job['link'] = u'http://upload.wikimedia.org/wikipedia/commons/2/26/YellowLabradorLooking_new.jpg'
		download_links.put(job)
	createImageFolder(u'hello')

eynyJobQueue = eynyBoss()
#debug()

# create worker and start them
workers = []
for i in range(5):
	workers.append(DownloadWorker(i, eynyJobQueue))
for i in range(5):
	workers[i].start()

# block until all the worker has done their job
gevent.joinall(workers)


