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

def create_bonding_task(params):
	
	bondid = params['bondid']
	commands = []
	commands.append("$SET interfaces bonding " + bondid)
	commands.append("$SET interfaces bonding %s address %s" % (bondid, params['address']))
	commands.append("$SET interfaces bonding %s mode %s" % (bondid, params['mode']))
	
	for ethernet in params['ethernets']:
		commands.append("$DELETE interfaces ethernet %s address" % ethernet)
		commands.append("$SET interfaces ethernet %s bound-group %s " % (ethernet, bondid))
	
	return FabricUtilNFV.send_vyatta_command(commands)

def create_bonding(id, params):
	
	logger.debug("create call!!")
	
	vm = get_vm(id)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(create_bonding_task, hosts=[addr], jsondata = params)

	return results[addr]
	
	
def update_bonding(params):
	
	logger.debug("update call!!")