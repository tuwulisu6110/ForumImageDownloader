from gevent import Greenlet, monkey
monkey.patch_all()
import requests
import os
from Job import Job

class DownloadWorker(Greenlet):
	store_dir = u'./temp/'
	session = requests.Session()
	def __init__(self, id=None, queue=None):
		Greenlet.__init__(self)
		self.workQueue = queue
		self.workerId = id

	def setQueue(self, queue):
		self.workQueue = queue
	
	def setId(self, id):
		self.workerId = id

	def _parseJob(self, job):
		self.urlLink = job.urlLink
		self.downloadFileName = os.path.join(self.store_dir, job.ImageFileName, u'{0:03}.jpg'.format(job.pageNumber))

	def _download(self):
		while not self.workQueue.empty():
			self._parseJob(self.workQueue.get_nowait())
			print u'worker {0} get job:'.format(self.workerId)
			r = self.session.get(self.urlLink, stream=True)	
			with open(self.downloadFileName, "w") as f:
				for chunk in r.iter_content(chunk_size=4096):
					if chunk:
						f.write(chunk)
			print u'worker {0} done job: {1} to {2}'.format(self.workerId, self.urlLink, self.downloadFileName)
	
	def _run(self):
		self._download()
