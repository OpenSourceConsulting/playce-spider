#-*- coding: utf-8 -*-
'''
Created on 2014. 9. 4.

@author: jerryj
'''
from flask import Flask, request, Response
import json
import uuid
from spidercore import *
from spidercore.FabricUtilKVM import *
from spidercore.FabricUtilNFV import *
from spidercore.service import NFVBondingService

logger = logging.getLogger(__name__)


@app.route("/vmreg", methods=['POST'])
def vm_reg_init():
	data = request.data
	sections = data.split('###')
	ifconfig = sections[1]
	route = sections[2]
	vbash = sections[3]
	uname = sections[4]
	
	# Parsing request data from a NFV VM that is trying to regster itself
	
	ifs = {}
	macaddrs = []
	ethName = None
	for line in ifconfig.split('\n'):
		sl = line.strip()
		if 'Link' in sl and 'Ethernet' in sl and 'HWaddr' in sl:
			ethName = sl.split()[0]
			macAddr = sl.split()[4]
#	 			print ethName, macAddr
			ifs[ethName] = {'macaddr': macAddr}
			macaddrs.append(macAddr)
		elif 'Link' in sl and 'Loopback' in sl:
				ethName = 'loopback'
				ifs['loopback'] = {}
		elif 'inet addr' in sl:
			ipAddr = sl.split()[1][5:]
# 			print ipAddr
			ifs[ethName]['ipaddr'] = ipAddr

	if 'loopback' in ifs:
		del ifs['loopback']
	
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
	
#	Asking which KVM Host host this NFV VM by matching MAC Addr

	vmhostId = None
	domain = None
	vmhosts = read_repository("vmhosts")
	results = []
	for vmhost in vmhosts:
		vms = getAllMacAddrs(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'])
		for vm in vms:
			print vm
			for mac in macaddrs:
				if mac in vm['macaddrs']:
					vmhostId = vmhost['_id']
					domain = vm['domain']
					break
	
	if vmhostId != None:
		vms = read_repository("vms")
		for i in range(0, len(vms)):
			vm = vms[i]
			if domain == vm['vmname']:
				if 'interim' in vm and vm['interim']:
					jsonData = {
						"_id": vm['_id'],
					    "vmhost": vmhostId,
					    "vyatta": isVyatta,
					    "vmname": domain,
					    "kernel": kernel,
					    "arch": arch,
					    "ostype": ostype,
					    "vmtype": "kvm",
					    "sshid": "vyos",
					    "sshpw": "vyos",
					    "interfaces": ifs,
					    "templateName": vm['templateName'],
					    "vendor": vm['vendor'],
					    "hostname": vm['hostname'],
					    "vmhostName": vm['vmhostName'],
					    "vmtype": vm['vmtype']
					}
					vms[i] = jsonData
					break
				else:
					return "DUP", 409
		
		# 	Seeking which interface can be communicated via management network
		for ifeth in ifs:
			if 'ipaddr' in ifs[ifeth]:
				ipAddr = ifs[ifeth]['ipaddr']
				if pingVM(ipAddr, jsonData['sshid'], jsonData['sshpw']):
					break
		else:
			return "FAIL: ping", 503
	
		#	Assign the unique VM is to NFV CollectD's hostname via Fabric
		#	SSH Account should be one for newly created VM
		
		try:
			jsonData['mgraddr'] = ipAddr
			initVM(ipAddr, jsonData['sshid'], jsonData['sshpw'], vm['_id'], jsonData['hostname'])
		except Exception, e:
			print e
			return "FAIL: init", 503

		#	Add new VM info to repository
		
		write_repository('vms', vms)

		return "OK", 200
	else:
		return "FAIL: No VMHost", 404

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
				results.append({'_id': vm['_id'], 'name': vm['vmname'], 'vmhost': vm['vmhost']})
			
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
			if id == vm['vmhost']:
				if request.args.get('detail', 'false').lower() in ['true', 'yes']:
					results.append(vm)
				else:
					results.append({'_id': vm['_id'], 'name': vm['vmname'], 'vmhost': vm['vmhost']})
					
		return json.dumps(results)
	else:
		return 'Not found', 404


@app.route("/mon/nfv/<id>/if/<ifid>", methods=['GET'])
def mon_vmif(id=None, ifid=None):
	if id == None:
		return "No unique id for VM", 404
	elif ifid == None:
		return "No unique ifid for interface", 404

	print "/mon/nfv/%s/if/%s" % (id, ifid)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			nics = getInterfaces(vm['mgraddr'], vm['sshid'], vm['sshpw'])
			for nic in nics:
				if ifid == '_all' or ifid == nic['ethName']:
					# DHCP일 경우 ifconfig로 주소, subnet 등을 읽어내는 코드가 필요
					# 그래서 json에 같이 병합해서 전송
					nicinfo = getIfConfig(vm['mgraddr'], vm['sshid'], vm['sshpw'], nic['ethName'])
					for kk in nicinfo:
						nic[kk] = nicinfo[kk]
					results.append(nic)

			return json.dumps(results)
	
	return 'Not found', 404


# nic 전체에 대한 config 정보를 통째로 받아 update
# repository 정보도 갱신
@app.route("/nfv/<id>/if/<ifid>", methods=['PUT'])
def vmifupdate(id=None, ifid=None):
	if id == None:
		return "No unique id for VM", 404
	elif ifid == None:
		return "No unique ifid for interface", 404

	logger.debug("/nfv/%s/if/%s" % (id, ifid))

	jsonData = json.loads(request.data)
	logger.debug(json.dumps(jsonData, indent=4))

	vms = read_repository("vms")
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			results = update_nic(vm['mgraddr'], vm['sshid'], vm['sshpw'], jsonData)
			break
	else:
		return "VM not found " + id, 404
	
	logger.debug(results)
	if "success" in results and results["success"] == "fail":
		return "Failed to update NIC %s" % ifid, 500
	
	for diff in results:
		ethName = diff["ethName"]
		if "hw-id" in diff:
			vm["interfaces"][ethName]["macaddr"] = diff["hw-id"]
		elif "address" in diff:
			if diff["address"] == "dhcp":
				nicinfo = getIfConfig(vm['mgraddr'], vm['sshid'], vm['sshpw'], ethName)
				vm["interfaces"][ethName]["ipaddr"] = nicinfo['ipaddr']
			else:
				vm["interfaces"][ethName]["ipaddr"] = diff["address"]
	
	return "OK", 200

# create bonding
@app.route("/nfv/<id>/bonding/<bondid>", methods=['POST', 'PUT'])
def vmbondingsave(id=None, bondid=None):
	if id == None:
		return "No unique id for VM", 500
	elif bondid == None:
		return "No unique bondid for interface", 500
	
	logger.debug("%s /nfv/%s/if/%s" % (request.method, id, bondid))
	jsonData = json.loads(request.data)
	logger.debug(json.dumps(jsonData, indent=4))
	
	if request.method == 'POST':
		NFVBondingService.create_bonding(jsonData)
	else:
		NFVBondingService.update_bonding(jsonData)
	
	return "OK", 200

@app.route("/mon/nfv/<id>/iflist", methods=['GET'])
def mon_vmiflist(id=None):
	if id == None:
		return "No unique id for VM", 404
	
	print "/mon/nfv/%s/iflist" % (id)

	results = {}
	
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from spidercore.FabricUtilNFV import getInterfaces
			nics = getInterfaces(vm['mgraddr'], vm['sshid'], vm['sshpw'])
			for nic in nics:
				results.append(nic['ethName'])
			return json.dumps(results)
	
	return 'Not found', 404




	
@app.route("/mon/nfv/<id>/nat/<rule>", methods=['GET'])
def mon_vmnat(id=None, rule=None):
	if id == None:
		return "No unique id for VM", 404
	elif rule == None:
		return "No unique rule for NAT", 404

	print "/mon/nfv/%s/nat/%s" % (id, rule)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from spidercore.FabricUtilNFV import getNATs
			nats = getNATs(vm['addr'], vm['sshid'], vm['sshpw'])
 			for nat in nats:
				if rule == '_all' or rule == nat['rule']:
 					results.append(nat)
			return json.dumps(results)
	
	return 'Not found', 404



	
@app.route("/mon/nfv/<id>/service/<svc>", methods=['GET'])
def mon_vmservice(id=None, svc=None):
	if id == None:
		return "No unique id for VM", 404
	elif svc == None:
		return "No unique svc for services", 404

	print "/mon/nfv/%s/service/%s" % (id, svc)

	results = {}
	
	vms = read_repository("vms")
	results = []
	for vm in vms:
		if '_id' in vm and id == vm['_id']:
			from spidercore.FabricUtilNFV import getServices
			services = getServices(vm['addr'], vm['sshid'], vm['sshpw'])
 			for service in services:
				if svc == '_all' or svc == service['service']:
 					results.append(service)
			return json.dumps(results)
	
	return 'Not found', 404