import gevent
import gevent.queue
from gevent import monkey
monkey.patch_all()

import os
import requests
from forum.eyny import eyny

download_links = gevent.queue.Queue()

# add some directory checking
def download(id):
	while not download_links.empty():
		link_obj = download_links.get()
		comic_title = link_obj['comicTitle']
		page = link_obj['page']
		link = link_obj['link']
		local_folder = u'./temp/{0}'.format(comic_title.replace('/','-'))
		print 'worker {0} get link....'.format(id)
		if not os.path.exists(local_folder):
			print u'creating {0} folder to store comic file...'.format(local_folder)
			os.makedirs(local_folder)

		# start download the file
		r = requests.get(link, stream=True)
		local_filename = u"{0}/{1}.jpg".format(local_folder, page)
		print u'downloading {0} as {1}...'.format(link, local_filename)
		with open(local_filename, "w") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)


def eynyBoss():
	eynyInstance = eyny()
	username = raw_input('username : ')
	password = raw_input('password : ')
	questionid = raw_input('question id : ')
	answer = raw_input('answer : ')
	try:
		eynyInstance.login(username, password, questionid=questionid, answer=answer)
		link_objs, comic_title = eynyInstance.parsing(u"http://www07.eyny.com/thread-9018016-1-2JSJRQNM.html")
		for lib_obj in link_objs:
			queue_obj = dict()
			queue_obj['comicTitle'] = comic_title
			queue_obj.update(lib_obj)
			download_links.put(queue_obj)
		
			
	finally:
		eynyInstance.logout()

eynyBoss()
workers = []
for i in range(5):
	workers.append(gevent.spawn(download, i))

gevent.joinall(workers)


