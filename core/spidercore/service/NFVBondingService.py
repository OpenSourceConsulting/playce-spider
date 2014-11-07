#-*- coding: utf-8 -*-
'''---------------------------------
	
	
	Created on 2014. 11. 5.
	@author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *
from fabric.api import env
from fabric.tasks import execute
import spidercore.FabricUtilNFV


logger = logging.getLogger(__name__)

def create_bonding_task(bondinfo):
	
	bondid = bondinfo['bondid']
	commands = []
	commands.append("$DELETE interfaces bonding " + bondid) # for test
	commands.append("$SET interfaces bonding " + bondid)
	commands.append("$SET interfaces bonding %s address %s" % (bondid, bondinfo['address']))
	commands.append("$SET interfaces bonding %s mode %s" % (bondid, bondinfo['mode']))
	
	for ethernet in bondinfo['ethernets']:
		commands.append("$DELETE interfaces ethernet %s address" % ethernet)
		commands.append("$SET interfaces ethernet %s bond-group %s " % (ethernet, bondid))
	
	return FabricUtilNFV.send_vyatta_command(commands)

def create_bonding(vmid, params):
	
	logger.debug("create call!!")
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(create_bonding_task, hosts=[addr], bondinfo = params)

	return results[addr]
	
def all_bonding(vmid):
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	result = []
	bond_dic = {}
	
	nics = FabricUtilNFV.getInterfaces(addr, vm['sshid'], vm['sshpw'])
	
	logger.debug(json.dumps(nics, indent=4))
	
	#bonging 정보만 추출.
	for nic in nics:
		if nic["ethName"].startswith("bond"):
			nic['items'] = []
			bond_dic[nic["ethName"]] = nic
		elif nic.has_key('bond-group'):
			bond_dic[nic["bond-group"]]['items'].append(nic["ethName"])
	
	for bond_id in bond_dic:
		result.append(bond_dic[bond_id])
	
	
	return result

def update_bonding(vmid, params):
	
	logger.debug("update call!!")
	
def delete_bonding_task(bondinfo):
	bondid = bondinfo['bondid']
	commands = []
	
	for eth in bondinfo["ethernets"]:
		commands.append("$DELETE interfaces ethernet %s bond-group" % eth) # for test
	
	commands.append("$DELETE interfaces bonding " + bondid) # for test
		
	return FabricUtilNFV.send_vyatta_command(commands)
	
def delete_bonding(vmid, params):
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(delete_bonding_task, hosts=[addr], bondinfo = params)

	return results[addr]