'''
Created on 2014. 10. 20.

@author: mwchoi
'''




from flask import Flask, request, Response
import json
import uuid
from spidercore import *
from spidercore.FabricUtilKVM2 import *



@app.route("/vm/clone", methods=['POST'])
def vm_clone():
	
	data = request.data
	jsonData = request.json
	vmHostId = jsonData['vmhost']
	
	template = jsonData['template']
	name = jsonData['newname']

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			jsonData['vmhostname'] = vmhost['name']
			vms = getDomcloneParamiko(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], template, name)
			found = True
	
	if found:
		vms = read_repository("vms")
		id = str(uuid.uuid4())
		jsonData['_id'] = id
		vms.append(jsonData)
		write_repository('vms', vms)
		return json.dumps({'_id': id})
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404
	

@app.route("/vm/templatelist/<vmHostId>", methods=['GET'])
def vm_template_list(vmHostId=None):

	if vmHostId == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getTemplatelist(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'])
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404



@app.route("/mon/vm/<vmHostId>/<name>/status", methods=['GET'])
def vm_state(vmHostId=None, name=None):

	if vmHostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404



# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404
	
	

@app.route("/mon/vm/<vmHostId>/<name>", methods=['GET'])
def vm_info(vmHostId=None, name=None):

	if vmHostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getDominfo(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404	




@app.route("/vm/start/<vmHostId>/<name>", methods=['GET'])
def vm_start(vmHostId=None, name=None):

	if vmHostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getDomstart(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404	




@app.route("/vm/shutdown/<vmHostId>/<name>", methods=['GET'])
def vm_shutdown(vmHostId=None, name=None):

	if vmHostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getDomshutdown(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404	



@app.route("/vm/define/<vmHostId>/<name>", methods=['GET'])
def vm_define(vmHostId=None, name=None):

	if vmHostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			vms = getDomdefine(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmHostId + ') was not found', 404	


