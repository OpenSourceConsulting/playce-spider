#-*- coding: utf-8 -*-
# ########################## Copyrights and license ############################################
#                                                                                              #
# Copyright 2014 Open Source Consulting, Inc. <support@osci.kr>                                #
#                                                                                              #
# This file is part of athena-spider. https://github.com/OpenSourceConsulting/athena-spider    #
#                                                                                              #
# athena-spider is free software: you can redistribute it and/or modify it under                    #
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
'''---------------------------------
	
	
	Created on 2014. 11. 14.
	@author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore.util import PyUtils

logger = logging.getLogger(__name__)

def get_ospf(vmid):
	
	logger.debug("get!!")

def save_ospf_task(ospf):
	commands = []
	
	for key in ospf:
		if '_' in key:
			_key = key.replace('_',' ')
		else:
			_key = key
			
		
		if len(ospf[key]) > 0:
			
			if key == 'parameters_router-id':
				commands.append("$SET interfaces loopback lo address %s" % ospf[key] )
			
			commands.append("$SET protocols ospf %s %s" % (_key, ospf[key]) )
		else:
			commands.append("$DELETE protocols ospf %s %s" % _key)
			
				
	return FabricUtilNFV.send_vyatta_command(commands)

def save_ospf(vmid, params):
	'''
	{
		'parameters_router-id' : '127.0.0.1',
		'auto-cost_reference-bandwidth' : 100,
		'default-methric' : 1
	}
	'''
	diff = PyUtils.diff_vyatta_conf(params['before'], params['after'])
	
	
	if len(diff) == 0:
		logger.debug("firewall 수정사항이 없습니다.")
		return {"success": "fail", "errmsg": "수정 사항이 없습니다."}
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(save_ospf_task, hosts=[addr], fwname=params['name'], ospf = diff)
	
	return results[addr]
	
def add_area(vmid):
	
	logger.debug("add_area!!")
	
def del_area(vmid):
	
	logger.debug("add_area!!")
	
'''	
def add_access(vmid, params):
	
	logger.debug("add_access!!")
	
def add_access(vmid, params):
	
	logger.debug("add_access!!")
	
def add_redist(vmid, params):
	
	logger.debug("add_redist!!")
'''