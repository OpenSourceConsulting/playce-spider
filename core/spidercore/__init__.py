from flask import Flask, request, Response
import os
import codecs
import json
from flask_cors import CORS
import logging.config
from pyparsing import *

#	Flask initialization
app = Flask(__name__)
cors = CORS(app, headers='Content-Type', methods=['HEAD', 'OPTIONS', 'POST', 'GET', 'DELETE', 'PUT'])

#	Main directory
mainDir = os.path.dirname(os.path.abspath(__file__))


keywords = CaselessKeyword('interfaces') | CaselessKeyword('nat') | CaselessKeyword('service') | CaselessKeyword('system')
elementList = Forward()
string = Word( alphanums+'_-:/.+@$' )
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                   Optional( '.' + Word(nums) ) +
                   Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
value = string | number | dblQuotedString.setParseAction(removeQuotes)
unaryItem = Group(value + Suppress(lineEnd()))
item = Group(string + value + Suppress(lineEnd()))
element = Forward()
itemOrElement = item | unaryItem | element
element << Group(string + Optional(string) + Group(Suppress('{') + ZeroOrMore(itemOrElement) + Suppress('}')))
elementList = ZeroOrMore(itemOrElement)
rootKeywords = keywords + Group( Suppress('{') + elementList + Suppress('}'))
config = OneOrMore(rootKeywords)
vbash_message = Regex(r"vbash\:.*").setName("vbash message")
config.ignore(vbash_message)


def convertNumbers(s,l,toks):
	n = toks[0]
	try:
		return int(n)
	except ValueError, ve:
		return float(n)
	
number.setParseAction( convertNumbers )



def setup_logging(
    default_path=mainDir+'/../conf/log_conf.json', 
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
	""" 
    Setup logging configuration
    """

	path = default_path
	print "setup_logging path: "+ os.path.abspath(path)
	value = os.getenv(env_key, None)
	if value:
		path = value
	if os.path.exists(path):
		with open(path, 'rt') as f:
			config = json.load(f)

		server_type = os.getenv("SVR_TYPE", None)

		if server_type:
			print "SVR_TYPE: " + server_type
			if "local" == server_type:
				config['handlers']['file_handler']['filename'] = "../spider.log";
				config['handlers']['error_file_handler']['filename'] = "../errors.log";
		else:
			print "SVR_TYPE is not set."
	
		logging.config.dictConfig(config)
		logging.info("logging: load "+ os.path.abspath(path))
	else:
		logging.basicConfig(level=default_level)
		logging.info("logging: set basic config.")

def read_repository(name):
	print "Name: " + name
	f = codecs.open(mainDir + '/' + name + ".json", 'r', encoding='utf8')
	data = f.read()
	f.close()
# 	print data
	jsonData = json.loads(data)
	return jsonData

def write_repository(name, data):
	print "Name: " + name
	f = codecs.open(mainDir + '/' + name + ".json", 'w', encoding='utf8')
	data = f.write(json.dumps(data))
	f.close()

setup_logging()
#logger = logging.getLogger(__name__)


