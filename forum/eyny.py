import requests
from lxml import etree, html
from forum import forum
import os


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
		response = self.session.get(url)
		htmldoc = etree.HTML(response.text)
		img_list = list()
		# image list parsing
		img_tags = htmldoc.xpath('//div[@class="pcb"]//td[@class="t_f"]//img')
		comic_title = htmldoc.xpath('//a[@id="thread_subject"]')
		for img_tag in img_tags:
			img_src = img_tag.get('src')
			if img_src.startswith('http') or img_src.startswith('https'):
				img_list.append(img_tag.get('src'))
		return img_list, comic_title[0].text


if __name__ == "__main__":
	print 'do not call this module directly'
