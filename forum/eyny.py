import requests
from lxml import etree, html
import time
from forum import forum
import os


class eyny(forum):
	def __init__(self):
		self.url = u'http://www01.eyny.com/'
		self.forum_name = u'Eyny'

	def login(self, username="", password="", **kargs):
		print '{0} login ....'.format(self.forum_name)
		path = u'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=Ld5u5&inajax=1'
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




# network login logout adult
# eyny.com login
# since eyny use other auth method, the **kargs is given.
#def login(session, username="", password="", **kargs):
#	url = u"http://www01.eyny.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=Ld5u5&inajax=1"
#	data = dict()
#	data['username'] = username
#	data['password'] = password
#	# current not support yet
#	data['questionid'] = kargs['questionid']
#	data['answer'] = kargs['answer']
#	response = session.post(url, data)
#
## some of the content in the forum are adult only
#def Adult(session):
#	url = u'http://www01.eyny.com/forum-1629-1.html'
#	data = {"agree": "yes"}
#	response = session.post(url, data)
#
## eyny.com logout
#def logout(session):
#	url = u"http://www01.eyny.com/member.php?mod=logging&action=logout&formhash=b6159313"
#	response = session.get(url)
#
#
## parsing the html file and dig the links
#def parsing(session, url):
#	response = session.get(url)
#	htmldoc = etree.HTML(response.text)
#	img_tags = htmldoc.xpath('//div[@class="pcb"]//td[@class="t_f"]//img')
#	img_list = list()
#	for img_tag in img_tags:
#		img_src = img_tag.get('src')
#		if img_src.startswith('http') or img_src.startswith('https'):
#			img_list.append(img_tag.get('src'))
#	return img_list

# add some directory checking
def download(url_list, comic_title):
	local_folder = u'./temp/{0}'.format(comic_title)
	os.mkdir(local_folder)
	for i in range(5):
	#for i in range(len(url_list)):
		r = requests.get(url_list[i], stream=True)
		local_filename = u"{0}/{1}.jpg".format(local_folder, i)
		print u'downloading {0} as {1}...'.format(url_list[i], local_filename)
		with open(local_filename, "w") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)

# the whole process should contain login, Adult, parsing and download
def debug():
	eynyInstance = eyny()
	username = raw_input('username : ')
	password = raw_input('password : ')
	questionid = raw_input('question id : ')
	answer = raw_input('answer : ')
	try:
		eynyInstance.login(username, password, questionid=questionid, answer=answer)
		link_list, comic_title = eynyInstance.parsing(u"http://www01.eyny.com/thread-9081711-1-3DN3CFFH.html")
	finally:
		eynyInstance.logout()

	download(link_list, comic_title)
def _debug():
	try:
		session = requests.Session()

		username = raw_input('username : ')
		password = raw_input('password : ')
		questionid = raw_input('question id : ')
		answer = raw_input('answer : ')

		login(session, username, password, questionid=int(questionid), answer=answer)
		Adult(session)
		url_list = parsing(session, u"http://www01.eyny.com/thread-8682090-1-3DN3CFFH.html")
		download(url_list)

	finally:
		logout(session)


if __name__ == "__main__":
	debug()
