
import pycurl
import urllib

class RelayReader:
	def __init__(self, relay):
		self.relay = urllib.urlopen(relay)
		
	def read_callback(self, size):
		return self.relay.read(size)
			

class Streamer(object):
	
	BUFFER_SIZE = 0x10000
	
	def __init__(self, host, port, mount_point, relay):
		self.host = host
		self.port = port
		self.mount_point = mount_point
		self.relay = relay
		self.url='http://'+self.host+':'+self.port+self.mount_point
		

	def stream(self):
		c = pycurl.Curl()
		c.setopt(pycurl.URL, self.url)
		c.setopt(pycurl.UPLOAD, 1)
		c.setopt(pycurl.READFUNCTION, RelayReader(self.relay).read_callback)
		c.perform()
		c.close()
		
s = Streamer('angus.parisson.com','8080','/publish/first?password=secret','http://127.0.0.1:9000/')
s.stream()


