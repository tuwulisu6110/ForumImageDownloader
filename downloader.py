import gevent
import gevent.queue
from gevent import monkey, Greenlet
monkey.patch_all()

import os
import os.path

import requests
from forum.eyny import eyny
from DownloadWorker import DownloadWorker


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
		link_objs, comic_title = eynyInstance.parsing(u"http://www09.eyny.com/thread-9361883-1-1.html")
		createImageFolder(comic_title)
		for lib_obj in link_objs:
			queue_obj = dict()
			queue_obj['comicTitle'] = comic_title.replace(u'/', u'-')
			queue_obj.update(lib_obj)
			download_links.put(queue_obj)
		
			
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
#eynyBoss()
debug()
workers = []
for i in range(5):
	workers.append(DownloadWorker(i, download_links))
for i in range(5):
	workers[i].start()

gevent.joinall(workers)


