import requests
import requests.utils
import pickle
import os.path

class forum(object):
	def __init__(self):
		self.url = u""
		self.session = requests.Session()

	# the cookie related method should be ok.
	# if the subclass wish to overwirte it, as you wish.
	# just remember what you are doing.

	# check whether the cookie is exist or not
	def _is_cookie_exist(self):
		# get the class name
		# the inherite class will also print it's name
		cookie_path = u'./cookie/{0}'.format(self.__class__.__name__)
		return os.path.exists(cookie_path)
	
	# store the cookie in the cookie path
	def _store_cookie(self):
		cookie_path = u'./cookie/{0}'.format(self.__class__.__name__)
		with open(cookie_path, 'w') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
	
	# load the cookie from the cookie path
	def _load_cookie(self):
		cookie_path = u'./cookie/{0}'.format(self.__class__.__name__)
		with open(cookie_path) as f:
			cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
		return cookies

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
