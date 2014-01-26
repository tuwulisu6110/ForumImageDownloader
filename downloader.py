import os
import requests
from forum.eyny import eyny

# add some directory checking
def download(url_list, comic_title):
	local_folder = u'./temp/{0}'.format(comic_title.replace('/','-'))
	if not os.path.exists(local_folder):
		print u'creating {0} folder to store comic file...'.format(local_folder)
		os.makedirs(local_folder)

	# start download the file
	for i in range(len(url_list)):
		r = requests.get(url_list[i], stream=True)
		local_filename = u"{0}/{1}.jpg".format(local_folder, i)
		print u'downloading {0} as {1}...'.format(url_list[i], local_filename)
		with open(local_filename, "w") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)


def debug():
	eynyInstance = eyny()
	username = raw_input('username : ')
	password = raw_input('password : ')
	questionid = raw_input('question id : ')
	answer = raw_input('answer : ')
	try:
		eynyInstance.login(username, password, questionid=questionid, answer=answer)
		link_list, comic_title = eynyInstance.parsing(u"http://www01.eyny.com/thread-9079503-1-3DN3CFFH.html")
	finally:
		eynyInstance.logout()

	download(link_list, comic_title)

debug()
