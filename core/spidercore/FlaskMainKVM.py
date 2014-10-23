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
	vmhostId = jsonData['vmhostId']
	
	template = jsonData['tname']
	name = jsonData['name']

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			jsonData['vmhostName'] = vmhost['name']
			vms = getDomcloneParamiko(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], template, name)
			found = True
	
	if found:
		vms = read_repository("vms")
		id = str(uuid.uuid4())
		jsonData['_id'] = id
		jsonData['vmhost'] = vmhostId
		jsonData['templateName'] = template
		del jsonData['vmhostId']
		del jsonData['tname']
		jsonData['interim'] = True
		vms.append(jsonData)
		write_repository('vms', vms)
		return json.dumps({'_id': id})
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404
	


@app.route("/vm/templatelist/<vmhostId>", methods=['GET'])
def vm_template_list(vmhostId=None):

	if vmhostId == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getTemplatelist(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'])
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404



@app.route("/mon/vm/<vmhostId>/<name>/status", methods=['GET'])
def vm_state(vmhostId=None, name=None):

	if vmhostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404



# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404
	
	

@app.route("/mon/vm/<vmhostId>/<name>", methods=['GET'])
def vm_info(vmhostId=None, name=None):

	if vmhostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getDominfo(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404	




@app.route("/vm/start/<vmhostId>/<name>", methods=['GET'])
def vm_start(vmhostId=None, name=None):

	if vmhostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getDomstart(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404	




@app.route("/vm/shutdown/<vmhostId>/<name>", methods=['GET'])
def vm_shutdown(vmhostId=None, name=None):

	if vmhostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getDomshutdown(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404	



@app.route("/vm/define/<vmhostId>/<name>", methods=['GET'])
def vm_define(vmhostId=None, name=None):

	if vmhostId == None:
		return "No unique id for VM", 404

	if name == None:
		return "No unique id for VM", 404

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			vms = getDomdefine(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			print vms
			found = True
	
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404	


