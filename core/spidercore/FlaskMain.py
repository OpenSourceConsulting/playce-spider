'''
Created on 2014. 9. 4.

@author: jerryj
'''
from flask import Flask, request, Response
import json
import uuid
from spidercore import *
from FlaskGraphite import *
from FlaskMainNFV import *
from FabricUtilKVM import *
from FlaskMainKVM import *
from FabricUtilKVM2 import *

@app.route("/shutdown", methods=['GET'])
def vmhost_shutdown():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	
#	Controller API

@app.route("/vmhost", methods=['POST'])
def vmhost_create():
	jsonData = request.json
# 	print 'JSON: ' + json.dumps(jsonData)
	name = jsonData['name']
	vmhosts = read_repository("vmhosts")

	token = str(uuid.uuid4())
	jsonData['_id'] = token;
	
	results = getAllInfo(jsonData['addr'], jsonData['sshid'], jsonData['sshpw'])
	jsonData['info'] = results['info']
	jsonData['version'] = results['version']
	jsonData['hostname'] = results['hostname']
	jsonData['interfaces'] = results['interfaces']
	
	newMacs = []
	for iff in jsonData['interfaces']:
		newMacs.append(iff['macaddr'])
	
	for vmhost in vmhosts:
		if name == vmhost['name']:
			return "Provided name is not unique", 409
		ifs = vmhost['interfaces']
		macs = []
		for iff in ifs:
			macs.append(iff['macaddr'])
		
		if set(newMacs) == set(macs):
			return "Alread registered VM Host", 409

	vmhosts.append(jsonData)
	write_repository('vmhosts', vmhosts)
	
	return json.dumps({'token': token})

# Deprecated
@app.route("/vmhost/<token>", methods=['PUT'])
def vmhost_register(token=None):
	jsonData = request.json
# 	print 'JSON: ' + json.dumps(jsonData)
	vmhosts = read_repository("vmhosts")
	for vmhost in vmhosts:
		if 'token' in vmhost:
			if token == vmhost['_id']:
# 				print vmhost['token']
				id = token
				vmhost['_id'] = id
				vmhost['hostname'] = jsonData['hostname']
				vmhost['type'] = jsonData['type']
				vmhost['addresses'] = jsonData['addresses']
				vmhost.pop('token')
	write_repository('vmhosts', vmhosts)
	return json.dumps({'_id': token})

@app.route("/vmhost/<id>", methods=['DELETE'])
def vmhost_delete(id = None):
	if id == None:
		return "No unique id for VM Host", 404

	vmhosts = read_repository("vmhosts")
	newVmhosts = []
	found = False
	for vmhost in vmhosts:
		if id == vmhost['_id']:
			found = True
		else:
			newVmhosts.append(vmhost)

	if found:
		write_repository("vmhosts", newVmhosts)
		return json.dumps({'_id': id})
	else:
		return "No unique id for VM Host", 404

@app.route("/vmhostbyname/<name>", methods=['GET'])
def vmhost_vmhostbyname(name = None):
	if name == None:
		return "No name has been provided", 404

	vmhosts = read_repository("vmhosts")
	for vmhost in vmhosts:
		print "%s:%s" % (name, vmhost['name'])
		if name == vmhost['name']:
			return json.dumps({'_id': vmhost['_id']})

	return "No VM Host found for provided name", 404

#	Monitoring API

@app.route("/mon/vmhost/<id>", methods=['GET'])
def mon_vmhost(id=None):
	if id == None:
		return "No unique id for VM Host", 404
	
	vmhosts = read_repository("vmhosts")
	results = []
	for vmhost in vmhosts:
		if '_id' in vmhost and (id == vmhost['_id'] or id == '_all'):
			if request.args.get('detail', 'false').lower() in ['true', 'yes']:
				results.append(vmhost)
			else:
				results.append({'_id': vmhost['_id'], 'name': vmhost['name'], 'location': vmhost['location']})
			
	return json.dumps(results)


if __name__ == "__main__":
	setup_logging()
	logger.critical('Server Starting...')
	app.run(host='0.0.0.0', port=5001, debug=True)





