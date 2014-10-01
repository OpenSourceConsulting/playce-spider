'''
Created on 2014. 9. 4.

@author: jerryj
'''
from flask import Flask, request, Response
import json
import uuid
from spidercore import *

@app.route("/vmreg", methods=['POST'])
def vm_reg_init():
	data = request.data
	sections = data.split('###')
	ifconfig = sections[1]
	route = sections[2]
	vbash = sections[3]
	uname = sections[4]
	
	ifs = {}
	ethName = None
	for line in ifconfig.split('\n'):
		sl = line.strip()
		if 'Link' in sl and 'Ethernet' in sl and 'HWaddr' in sl:
			ethName = sl.split()[0]
			macAddr = sl.split()[4]
# 			print ethName, macAddr
			ifs[ethName] = {'macaddr': macAddr}
		elif 'inet addr' in sl:
			ipAddr = sl.split()[1][5:]
# 			print ipAddr
			if 'ipaddr' not in ifs[ethName]:
				ifs[ethName]['ipaddr'] = ipAddr
	
	for line in route.split('\n'):
		words = line.strip().split()
		if len(words) == 8:
			ethName = words[7]
# 			print ethName
			if ethName in ifs:
				if 'routes' not in ifs[ethName]:
					ifs[ethName]['routes'] = []
				ifs[ethName]['routes'].append({'destination': words[0], 'gateway': words[1]})
	
	line = uname.split('\n')[1]
	words = line.split()
	hostname = words[1]
	kernel = words[2]
	arch = words[-2]
	ostype = words[-1]
	isVyatta = False

	if 'vyatta' in kernel.lower():
		isVyatta = True
		vbashVersion = None
		for line in vbash.split('\n'):
			if 'gnu bash' in line.lower():
				vbashVersion = line.split()[3]

	print json.dumps(ifs, indent=4)
	print "Hostname: %s, Kernel: %s, Arch: %s, OsType: %s" % (hostname, kernel, arch, ostype)
	print "Vyatta: %s" % isVyatta
	

	return "OK"

@app.route("/vm", methods=['POST'])
def vm_register():
	data = request.data
# 	print 'Data: ' + data
	jsonData = request.json
# 	print 'JSON: ' + json.dumps(jsonData)
	vmHostId = jsonData['vmhost']
	name = jsonData['name']
	
# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
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

@app.route("/vm/<id>", methods=['DELETE'])
def vm_delete(id = None):
	if id == None:
		return "No unique id for VM", 404

	vms = read_repository("vms")
	newVms = []
	found = False
	for vm in vms:
		if id == vm['_id']:
			found = True
		else:
			newVms.append(vm)

	if found:
		write_repository("vms", newVms)
		return json.dumps({'_id': id})
	else:
		return "No unique id for VM", 404

#	Monitoring API

@app.route("/mon/vm/<id>", methods=['GET'])
def mon_vm(id=None):
	if id == None:
		return "No unique id for VM", 404
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and (id == vm['_id'] or id == '_all'):
			if request.args.get('detail', 'false').lower() in ['true', 'yes']:
				results.append(vm)
			else:
				results.append({'_id': vm['_id'], 'name': vm['name'], 'vmhost': vm['vmhost']})
			
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

# 	print "vmhostName: " + vmhostName
	
	if vmhostName != None:
		vms = read_repository("vms")
		results = []
		for vm in vms:
			print vm['vmhost']
			if vmhostName == vm['vmhost']:
				if request.args.get('detail', 'false').lower() in ['true', 'yes']:
					results.append(vm)
				else:
					results.append({'_id': vm['_id'], 'name': vm['name'], 'vmhost': vm['vmhost']})
					
		return json.dumps(results)
	else:
		return 'Not found', 404


@app.route("/mon/vm/<id>/if/<ifid>", methods=['GET'])
def mon_vmif(id=None, ifid=None):
	if id == None:
		return "No unique id for VM", 404
	elif ifid == None:
		return "No unique ifid for interface", 404

	print "/mon/vm/%s/if/%s" % (id, ifid)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from FabricUtil import getInterfaces
			nics = getInterfaces(vm['addr'], vm['sshid'], vm['sshpw'])
			for nic in nics:
				if ifid == '_all' or ifid == nic['ethName']:
					results.append(nic)
			return json.dumps(results)
	
	return 'Not found', 404
	
@app.route("/mon/vm/<id>/nat/<rule>", methods=['GET'])
def mon_vmnat(id=None, rule=None):
	if id == None:
		return "No unique id for VM", 404
	elif rule == None:
		return "No unique rule for NAT", 404

	print "/mon/vm/%s/nat/%s" % (id, rule)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from FabricUtil import getNATs
			nats = getNATs(vm['addr'], vm['sshid'], vm['sshpw'])
 			for nat in nats:
				if rule == '_all' or rule == nat['rule']:
 					results.append(nat)
			return json.dumps(results)
	
	return 'Not found', 404
	
@app.route("/mon/vm/<id>/service/<svc>", methods=['GET'])
def mon_vmservice(id=None, svc=None):
	if id == None:
		return "No unique id for VM", 404
	elif svc == None:
		return "No unique svc for services", 404

	print "/mon/vm/%s/service/%s" % (id, svc)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from FabricUtil import getServices
			services = getServices(vm['addr'], vm['sshid'], vm['sshpw'])
 			for service in services:
				if svc == '_all' or svc == service['service']:
 					results.append(service)
			return json.dumps(results)
	
	return 'Not found', 404
	
