'''
Created on 2014. 9. 4.

@author: jerryj
'''
from flask import Flask, request, Response, jsonify
import json
import codecs
import uuid
import requests

app = Flask(__name__)

def read_repository(name):
	print "Name: " + name
	f = codecs.open(name + ".json", 'r', encoding='utf8')
	data = f.read()
	f.close()
# 	print data
	jsonData = json.loads(data)
	return jsonData

def write_repository(name, data):
	print "Name: " + name
	f = codecs.open(name + ".new.json", 'w', encoding='utf8')
	data = f.write(json.dumps(data))
	f.close()

@app.route("/shutdown", methods=['GET'])
def vmhost_shutdown():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	
#	Controller API

@app.route("/vmhost/register", methods=['POST'])
def vmhost_register():
	data = request.data
	print 'Data: ' + data
	jsonData = request.json
	print 'JSON: ' + json.dumps(jsonData)
	token = jsonData['token']
	vmhosts = read_repository("vmhosts")
	for vmhost in vmhosts:
		if 'token' in vmhost:
			if token == vmhost['token']:
				print vmhost['token']
				id = str(uuid.uuid4())
				vmhost['_id'] = id
				vmhost['hostname'] = jsonData['hostname']
				vmhost['type'] = jsonData['type']
				vmhost['addresses'] = jsonData['addresses']
				vmhost.pop('token')
	write_repository('vmhosts', vmhosts)
	return json.dumps({'_id': id})

@app.route("/vm/register", methods=['POST'])
def vm_register():
	data = request.data
	print 'Data: ' + data
	jsonData = request.json
	print 'JSON: ' + json.dumps(jsonData)
	vmhostName = jsonData['vmhost']
	hostname = jsonData['hostname']
	
# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['name'] == vmhostName:
			found = True
	
	if found:
		vms = read_repository("vms")
		id = str(uuid.uuid4())
		jsonData['_id'] = id
		jsonData['name'] = vmhostName + '-' + hostname
		vms.append(jsonData)
		write_repository('vms', vms)
		return json.dumps({'_id': id})
	else:
		return 'VM Host(' + vmhostName + ') was not found', 404

#	Monitoring API

@app.route("/mon/vmhost/<id>", methods=['GET'])
def mon_vmhost(id=None):
	if id == None:
		return "No unique id for VM Host", 404
	
	vmhosts = read_repository("vmhosts")
	results = []
	for vmhost in vmhosts:
		if '_id' in vmhost and id == vmhost['_id']:
			results.append(vmhost)
		elif id == '_all':
			results.append(vmhost)
			
	return json.dumps(results)

@app.route("/mon/vm/<id>", methods=['GET'])
def mon_vm(id=None):
	if id == None:
		return "No unique id for VM Host", 404
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			results.append(vm)
		elif id == '_all':
			results.append(vm)
			
	return json.dumps(results)

@app.route("/mon/vmbyhost/<id>", methods=['GET'])
def mon_vmbyhost(id=None):
	if id == None:
		return "No unique id for VM Host", 404
	
	vmhosts = read_repository("vmhosts")
	vmhostName = None
	for vmhost in vmhosts:
		if '_id' in vmhost and id == vmhost['_id']:
			vmhostName = vmhost['name']

	print "vmhostName: " + vmhostName
	
	if vmhostName != None:
		vms = read_repository("vms")
		results = []
		for vm in vms:
			print vm['vmhost']
			if vmhostName == vm['vmhost']:
				results.append(vm)
					
		return json.dumps(results)
	else:
		return 'Not found', 404
		

#	Monitoring API

@app.route("/mon/graphite", methods=['GET'])
def mon_graphite():
	queryStr = request.query_string
	result = requests.get('http://192.168.56.12:8000/render?' + queryStr + '&format=json').json()
	for metric in result:
		datapoints = metric['datapoints']
		newDatapoints = []
		for val in datapoints:
			newVal = { "value": val[0], "date": val[1]}
			newDatapoints.append(newVal)
		metric['datapoints'] = newDatapoints
	return json.dumps(result) + '\n'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)






