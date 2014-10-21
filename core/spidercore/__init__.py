from flask import Flask, request, Response
import os
import codecs
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, headers='Content-Type', methods=['HEAD', 'OPTIONS', 'POST', 'GET', 'DELETE', 'PUT'])

mainDir = os.path.dirname(os.path.abspath(__file__))

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

