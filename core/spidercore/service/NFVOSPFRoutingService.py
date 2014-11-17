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

def parse_ospf_list(list):
	results = []
	for item in list[2]:
		area = {}
		area[list[0]] = list[1]
		area[item[0]] = item[1]
		results.append(area)
	return results

def get_ospf(vmid):
	
	result = FabricUtilNFV.get_vyatta_conf(vmid, "$SHOW protocols ospf")
	
	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	print '------------------------------'
	
	result = {"areas":[], "access-list":[], "redist-list":[]}
	for depth1 in results.asList():
		if depth1[0] in ['auto-cost','parameters']:
			result[depth1[0] + "_" + depth1[1][0][0]] = depth1[1][0][1]
			
		elif 'area' == depth1[0]:
			result['areas'].extend(parse_ospf_list(depth1))
		elif 'access-list' == depth1[0]:
			result['access-list'].extend(parse_ospf_list(depth1))
		elif 'redistribute' == depth1[0]:
			for item in depth1[1]:
				prot = {}
				prot['protocol'] = item[0]
				for item2 in item[1]:
					prot[item2[0]] = item2[1]
				result['redist-list'].append(prot)
		else:
			result[depth1[0]] = depth1[1]
			
		
	return {"success":"success", "msg":json.dumps(result)}

def save_ospf_task(ospf):
	commands = []
	
	for key in ospf:
		if '_' in key:
			_key = key.replace('_',' ')
		else:
			_key = key
			
		
		if len(ospf[key]) > 0:
			
			if key == 'parameters_router-id':
				commands.append("$SET interfaces loopback lo address %s/24" % ospf[key] )
			
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
	results = execute(save_ospf_task, hosts=[addr], ospf = diff)
	
	return results[addr]
	
def add_area_task(ospf):
	commands = []
	
	commands.append("$SET protocols ospf area %s network %s" % (ospf['area'], ospf['network']) )
		
	return FabricUtilNFV.send_vyatta_command(commands)
	
def add_area(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(add_area_task, hosts=[addr], ospf = params)
	
	return results[addr]

def del_area_task(ospf):
	commands = []
	
	commands.append("$DELETE protocols ospf area %s network %s" % (ospf['area'], ospf['network']) )
		
	return FabricUtilNFV.send_vyatta_command(commands)
	
def del_area(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(del_area_task, hosts=[addr], ospf = params)
	
	return results[addr]
	
def add_access_task(ospf):
	commands = []
	
	commands.append("$SET protocols ospf access-list %s export %s" % (ospf['access-list'], ospf['export']) )
		
	return FabricUtilNFV.send_vyatta_command(commands)

def add_access(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(add_access_task, hosts=[addr], ospf = params)
	
	return results[addr]
	
def del_access_task(ospf):
	commands = []
	
	commands.append("$DELETE protocols ospf access-list %s export %s" % (ospf['access-list'], ospf['export']) )
		
	return FabricUtilNFV.send_vyatta_command(commands)

def del_access(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(del_access_task, hosts=[addr], ospf = params)
	
	return results[addr]

def add_redist_task(ospf):
	commands = []
	
	commands.append("$SET protocols ospf redistribute %s" % ospf['protocol'] )
	
	if 'metric' in ospf and len(ospf['metric']) > 0:
		commands.append("$SET protocols ospf redistribute %s metric %s" % (ospf['protocol'], ospf['metric']) )
		
	if 'metric-type' in ospf and len(ospf['metric-type']) > 0:
		commands.append("$SET protocols ospf redistribute %s metric-type %s" % (ospf['protocol'], ospf['metric-type']) )
		
	if 'route-map' in ospf and len(ospf['route-map']) > 0:
		commands.append("$SET protocols ospf redistribute %s route-map %s" % (ospf['protocol'], ospf['route-map']) )
		
	return FabricUtilNFV.send_vyatta_command(commands)
	
def add_redist(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(add_redist_task, hosts=[addr], ospf = params)
	
	return results[addr]

def del_redist_task(ospf):
	commands = []
	
	commands.append("$DELETE protocols ospf redistribute %s" % ospf['protocol'] )
		
	return FabricUtilNFV.send_vyatta_command(commands)

def del_redist(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(del_redist_task, hosts=[addr], ospf = params)
	
	return results[addr]
