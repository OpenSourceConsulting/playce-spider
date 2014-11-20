#-*- coding: utf-8 -*-
# ########################## Copyrights and license ############################################
#                                                                                              #
# Copyright 2014 Open Source Consulting, Inc. <support@osci.kr>                                #
#                                                                                              #
# This file is part of athena-spider. https://github.com/OpenSourceConsulting/athena-spider    #
#                                                                                              #
# athena-spider is free software: you can redistribute it and/or modify it under               #
# the terms of the GNU Lesser General Public License as published by the Free                  #
# Software Foundation, either version 3 of the License, or (at your option)                    #
# any later version.                                                                           #
#                                                                                              #
# athena-spider is distributed in the hope that it will be useful, but WITHOUT ANY             #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS                    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more                 #
# details.                                                                                     #
#                                                                                              #
# You should have received a copy of the GNU Lesser General Public License                     #
# along with athena-spider. If not, see <http://www.gnu.org/licenses/>.                        #
#                                                                                              #
# ##############################################################################################
'''
Created on 2014. 10. 20.

@author: mwchoi
'''


from flask import Flask, request, Response
import json
import uuid
from spidercore import *
from spidercore.FabricUtilKVM2 import *
from spidercore.util import PyUtils


logger = logging.getLogger(__name__)


@app.route("/vm/clone", methods=['POST'])
def vm_clone():
	
	data = request.data
	jsonData = request.json
	vmhostId = jsonData['vmhostId']
	
	template = jsonData['tname']
	name = jsonData['name']
	
	vms = read_repository("vms")
	for vm in vms:
		if name == vm['vmname'] and vmhostId == vm['vmhost']:
			return "Provided name is already exists.", 409

	# Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmhostId:
			jsonData['vmhostName'] = vmhost['name']
			getDomcloneParamiko(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], template, name)
			found = True
	
	if found:
		vms = read_repository("vms")
		id = str(uuid.uuid4())
		jsonData['_id'] = id
		jsonData['vmhost'] = vmhostId
		jsonData['templateName'] = template
		jsonData['vmname'] = name
		del jsonData['vmhostId']
		del jsonData['tname']
		del jsonData['name']
		
		jsonData['interim'] = True
		vms.append(jsonData)
		write_repository('vms', vms)
		return json.dumps({'_id': id}), 200
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404
	

@app.route("/vm/<id>", methods=['DELETE'])
def vm_delete(id = None):
	if id == None:
		return "No unique id for VM", 404

	vmhost = findVmhostById(id)
	existvm = findVmById(id)
	newVms = []

	if 'No unique' in vmhost:
		return "No unique name for VM : " + existvm['vmname'] , 404
	else:
		deletevm = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], existvm['vmname'])
		delvm_status = deletevm[0]['state']

		found = False
		if 'running' in delvm_status:
			return "["+id+"] is already running", 409
		else:

			deletevm = getDomremove(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], existvm['vmname'])
			print deletevm
					
			found = False			
			readvms = read_repository("vms")
			for vm in readvms:
				if id == vm['_id']:
					found = True
				else:
					newVms.append(vm)

			write_repository("vms", newVms)
			
			return 'VM (' + id + ') is remove complete', 200
		


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
			found = True
			vms = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
			if 'state' in vms[0] and vms[0]['state'] != 'running':
				vms[0]['clone_state'] = getClonestate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], name)
			
	if found:
		return json.dumps(vms)
	else:
		return 'VM Host(' + vmhostId + ') was not found', 404


@app.route("/mon/vm/all/status", methods=['GET'])
def vm_all_state():

	vmList = read_repository("vms")
	vms = {"vms":[]}
	for vm in vmList:
		if PyUtils.isEquals(vm, "interim", True):
			vms[vm["vmname"]] = True # interim 이 true 일때 {"vm1":true} 로 setting.
		else:
			vms[vm["vmname"]] = False
		vms["vms"].append(vm["vmname"])

# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	
	result = []
	for vmhost in vmhosts:
		state = {"vmhost":vmhost["name"]}
		state["vms"] = getVmAllState(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], vms)
		result.append( state )
	
	if len(result) > 0:
		return json.dumps(result), 200
	else:
		return 'VM Host was not found', 500

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
		return json.dumps(vms) , 200
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
		return json.dumps(vms) , 200
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






def findByVmhost(vmname):

	if vmname == None:
		return "No unique id for VM"

# 	Finding a VM Host designated in the JSON request
	vms = read_repository("vms")
	found = False
	vmhostId = None
	vmhost = None
	
	for vm in vms:
		if vm['vmname'] == vmname:
			found = True
			vmhostId = vm['vmhost']

	if found:
		vmhosts = read_repository("vmhosts")
		for tmpvmhost in vmhosts:
			if tmpvmhost['_id'] == vmhostId:
				vmhost = tmpvmhost
				break
		return vmhost
	else:
		return "No unique id for VM"




def findVmhostById(id):

	if id == None:
		return "No unique id for VM"

# 	Finding a VM Host designated in the JSON request
	vms = read_repository("vms")
	found = False
	vmhostId = None
	vmhost = None
	
	for vm in vms:
		if vm['_id'] == id:
			found = True
			vmhostId = vm['vmhost']

	if found:
		vmhosts = read_repository("vmhosts")
		for tmpvmhost in vmhosts:
			if tmpvmhost['_id'] == vmhostId:
				vmhost = tmpvmhost
				break
		return vmhost
	else:
		return "No unique id for VM"


def findVmById(id):

	if id == None:
		return "No unique id for VM"

# 	Finding a VM Host designated in the JSON request
	vms = read_repository("vms")
	found = False
	vmhostId = None
	vmhost = None
	retrunvm = None

	found = False	
	for vm in vms:
		if vm['_id'] == id:
			retrunvm = vm
			found = True
			break

	if found:
		return retrunvm
	else:
		return "No unique id for VM"




