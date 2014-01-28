class Job(object):
	def __init__(self, ImageFileName=u'', pageNumber=None, urlLink=u''):
		self.content = dict()
		self.content['ImageFileName'] = ImageFileName.replace('/', '-')
		self.content['pageNumber'] = pageNumber
		self.content['urlLink'] = urlLink
	@property	
	def ImageFileName(self):
		return self.content['ImageFileName']

	@ImageFileName.setter
	def ImageFileName(self, fileName):
		self.content['ImageFileName'] = fileName
	
	@property
	def pageNumber(self):
		return self.content['pageNumber']
	
	@pageNumber.setter
	def pageNumber(self, page):
		self.content['pageNumber'] = page

	@property
	def urlLink(self):
		return self.content['urlLink']

	@urlLink.setter
	def urlLink(self, link):
		self.content['urlLink'] = link
	
