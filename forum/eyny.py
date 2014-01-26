import requests
from lxml import etree, html
import time

# This should be change into an class.
# with login, logout, Adult, parsing as virtual function.
# some other filed should be added later



# network login logout adult
# eyny.com login
# since eyny use other auth method, the **kargs is given.
def login(session, username="", password="", **kargs):
	url = u"http://www01.eyny.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=Ld5u5&inajax=1"
	data = dict()
	data['username'] = username
	data['password'] = password
	# current not support yet
	data['questionid'] = kargs['questionid']
	data['answer'] = kargs['answer']
	response = session.post(url, data)

# some of the content in the forum are adult only
def Adult(session):
	url = u'http://www01.eyny.com/forum-1629-1.html'
	data = {"agree": "yes"}
	response = session.post(url, data)

# eyny.com logout
def logout(session):
	url = u"http://www01.eyny.com/member.php?mod=logging&action=logout&formhash=b6159313"
	response = session.get(url)


# parsing the html file and dig the links
def parsing(session, url):
	response = session.get(url)
	htmldoc = etree.HTML(response.text)
	img_tags = htmldoc.xpath('//div[@class="pcb"]//td[@class="t_f"]//img')
	img_list = list()
	for img_tag in img_tags:
		img_src = img_tag.get('src')
		if img_src.startswith('http') or img_src.startswith('https'):
			img_list.append(img_tag.get('src'))
	return img_list

# add some directory checking
def download(url_list):
	local_folder = './temp/comicname'
	for i in range(5):
	#for i in range(len(url_list)):
		r = requests.get(url_list[i], stream=True)
		local_filename = "{0}/{1}.jpg".format(local_folder, i)
		print 'downloading {0} as {1}...'.format(url_list[i], local_filename)
		with open(local_filename, "w") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)

# the whole process should contain login, Adult, parsing and download
def debug():
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
