
import httplib
import os
import pycurl
import urllib

class FileReader:
	def __init__(self, fp):
		self.fp = fp

	def read_callback(self, size):
		return self.fp.read(size)

class RelayReader:
	def __init__(self, relay):
		self.relay = urllib.urlopen(relay)
		
	def read_callback(self, size):
		return self.relay.read(size)
			

class Streamer(object):
	
	BUFFER_SIZE = 0x10000
	
	def __init__(self, host, port, mount_point, media, relay):
		self.host = host
		self.port = port
		self.mount_point = mount_point
		self.media = media
		self.relay = relay
		
		self.file = open(self.media, 'r')
		self.url='http://'+self.host+':'+self.port+self.mount_point
		
	def read(self):
		while True:
			buf = self.file.read(self.BUFFER_SIZE)
			if not len(buf):
				break
			yield buf
					
	def stream(self):
		feed = self.read()
		h = httplib.HTTPConnection(self.host,self.port)
		for buf in feed:
			h.request('POST',self.mount_point)
			h.send(buf)
			response = h.getresponse()
			#print response
			#print response.status, response.reason, response.read()

	def stream2(self):
		c = pycurl.Curl()
		c.setopt(pycurl.URL, self.url)
		c.setopt(pycurl.UPLOAD, 1)
		#c.setopt(pycurl.READFUNCTION, FileReader(self.file).read_callback)
		#c.setopt(pycurl.READFUNCTION, self.file.read)
		c.setopt(pycurl.READFUNCTION, RelayReader(self.relay).read_callback)
		#filesize = os.path.getsize(self.media)
		#c.setopt(pycurl.INFILESIZE, filesize)
		c.perform()
		c.close()
		
s = Streamer('127.0.0.1','9080','/publish/first?password=secret','/home/momo/Downloads/test.webm','http://192.168.0.14:9000/')
s.stream2()


