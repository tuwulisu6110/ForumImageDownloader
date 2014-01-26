import requests

class forum(object):
	url = u""
	session = requests.Session()
	
	# the subclass should implement the following method,
	# since most forum will have different login logout mechanism.
	# Moreover, the html format will also changed depending on the website.
	# Therefore, it's the subclass's job to implement such kind of method.
	def login(self, username, password, **kargs):
		raise NotImplemented()
	
	def logout(self):
		raise NotImplemented()
	
	def parsing(self):
		raise NotImplemented()
	
	def help(self):
		raise NotImplemented()
