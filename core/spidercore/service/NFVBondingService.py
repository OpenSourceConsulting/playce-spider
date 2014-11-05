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

def create_bonding(id, params):
	
	logger.debug("create call!!")
	
	vm = get_vm(id)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(create_bonding_task, hosts=[addr], bondinfo = params)

	return results[addr]
	
	
def update_bonding(id, params):
	
	logger.debug("update call!!")