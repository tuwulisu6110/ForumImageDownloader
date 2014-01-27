from gevent.queue import Queue as geventQueue
import requests
from lxml import etree, html
import os

from forum import forum
from company.Job import Job


class eyny(forum):
	def __init__(self):
		self.url = u'http://www01.eyny.com/'
		self.forum_name = u'Eyny'

	def login(self, username="", password="", **kargs):
		print '{0} login ....'.format(self.forum_name)
		path = u'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&inajax=1'
		login_url = self.url + path
		data = dict()
		data['username'] = username
		data['password'] = password
		# put other argument inside the data dictionary
		data.update(kargs)
		response = self.session.post(login_url, data)
		self._Adult()
	
	def _Adult(self):
		path = u'forum-1629-1.html'
		Adult_url = self.url + path
		data = {"agree": "yes"}
		response = self.session.post(Adult_url, data)
	
	def logout(self):
		print '{0} logout....'.format(self.forum_name)
		path = u"member.php?mod=logging&action=logout&formhash=b6159313"
		logout_url = self.url + path
		response = self.session.get(logout_url)
	
	# right now it only support the hcmoic session :)
	def parsing(self, url):
		JobQueue = geventQueue()
		response = self.session.get(url)
		htmldoc = etree.HTML(response.text)
		# lxml parsing
		img_tags = htmldoc.xpath('//div[@class="pcb"]//td[@class="t_f"]//img')
		comic_title = htmldoc.xpath('//a[@id="thread_subject"]')[0].text
		
		# creating JobQueue for workers
		# each parsing will create a new JobQueue 
		img_srcs = [src.get('src') for src in img_tags if src.get('src').startswith('http') or src.get('src').startswith('https')]
		for page, link in enumerate(img_srcs):
			JobQueue.put(Job(comic_title, page, link))


		return comic_title, JobQueue


if __name__ == "__main__":
	print 'do not call this module directly'
