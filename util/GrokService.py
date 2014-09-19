import rpyc
from rpyc.utils.server import ThreadedServer
import libgrok
import sys
import json

class GrokService(rpyc.core.service.Service):
	g = None

	def init(self):
		if self.g == None:
			self.g = libgrok.Grok()
			self.g.add_patterns_from_file('/usr/share/grok/patterns/base')

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def exposed_add_pattern(self, name, pattern):
		self.init()
		self.g.add_pattern(name, pattern)

	def exposed_parse(self, text, pattern):
		self.init()
		self.g.compile(pattern)
		match = libgrok.MatchResult()
		result = self.g(text, match)
		if result == 0:
			return json.dumps(self.g.parse(match))
		else:
			return None

	def get_question(self):
		return "what is the airspeed velocity of an unladen swallow?"

if __name__ == "__main__":
	t = ThreadedServer(GrokService, port=18881)
	t.start()



