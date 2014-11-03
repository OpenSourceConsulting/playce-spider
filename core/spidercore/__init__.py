from flask import Flask, request, Response
import os
import codecs
import json
from flask_cors import CORS
import logging.config

app = Flask(__name__)
cors = CORS(app, headers='Content-Type', methods=['HEAD', 'OPTIONS', 'POST', 'GET', 'DELETE', 'PUT'])

mainDir = os.path.dirname(os.path.abspath(__file__))

def setup_logging(
    default_path='conf/log_conf.json', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """ 
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
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

