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
	
	
	Created on 2014. 11. 12.
	@author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore.util import PyUtils

logger = logging.getLogger(__name__)


def validate_params(params):
	
	for key in params:
		if 'protocol' == key and params['protocol'].lower() in ['tcp','udp']:
			if len(params['source_port']) == 0 and len(params['source_port']) == 0:
				raise ValueError('protocol 이 TCP, UDP 일때는 port 도 지정해야 합니다.')
	
	return None

def get_firewall(vmid, fwname):
	
	return {"success":"success","msg":"Not Implemented"}

def create_firewall_task(fwinfo):
	
	fwname = fwinfo['name']
	
	# 무조건 생성 (already exists 무시)
	FabricUtilNFV.send_vyatta_command(['$SET firewall name '+fwname])
	
	commands = []
	rule_num = fwinfo['rule']
	
	commands.append("$DELETE firewall name %s rule %s " % (fwname, rule_num))
	commands.append("$SET firewall name %s rule %s " % (fwname, rule_num))
	
	for key in fwinfo:
		if '_' in key:
			_key = key.replace('_',' ')
		else:
			_key = key
			
		if key in ['rule','ethernet','inout', 'name']:
			continue
			
		if len(fwinfo[key]) > 0:
			commands.append("$SET firewall name %s rule %s %s %s " % (fwname, rule_num, _key, fwinfo[key]))
		
	if 'ethernet' in fwinfo:
		commands.append("$SET interfaces ethernet %s firewall %s name %s " % (fwinfo['ethernet'], fwinfo['inout'], fwname))
	
	return FabricUtilNFV.send_vyatta_command(commands)

def create_firewall(vmid, params):
	
	vm = get_vm(vmid)
	
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	
	results = execute(create_firewall_task, hosts=[addr], fwinfo = params)

	return results[addr]
	
def get_firewall_nic(nics, fwname):
	
	result = {}
	for nic in nics:
		if 'firewall' in nic and nic['firewall'][1] == fwname:
			result['ethernet'] = nic['ethName']
			result['inout'] = nic['firewall'][0]
	
	return result

def all_firewall(vmid):
	
	result = FabricUtilNFV.get_vyatta_conf(vmid, "$SHOW firewall name")
	
	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	
	vm = get_vm(vmid)
	nics = FabricUtilNFV.getInterfaces(vm['mgraddr'], vm['sshid'], vm['sshpw'], 'ethernet')
	
	print '------------------------------'
	
	fws = []
	for depth1 in results.asList():
		fw = {depth1[0]: depth1[1], 'rules':[]} # {'name':'FWTEST-1', 'rules':[]}
		
		fw.update(get_firewall_nic(nics, depth1[1]))
		
		for depth2 in depth1[2]:
			rule = {}
			if len(depth2) == 2:
				fw[depth2[0]] = depth2[1] # {'default-action':'drop'}
				
			elif len(depth2) == 3:
				rule[depth2[0]] = depth2[1] # {'rule':'3'}
				
				for depth3 in depth2[2]:
					if type(depth3[1]) is str:
						rule[depth3[0]] = depth3[1]
						
					else:
						for depth4 in depth3[1]:
							if type(depth4[1]) is str:
								rule[depth3[0]+"_"+depth4[0]] = depth4[1] #['state', [['established', 'enable'], ['related', 'enable']]]]],
							else:
								rule[depth3[0]+"_"+depth4[0]] = depth4[1][0][1] # ['source', [['group', [['address-group', 'SERVERS']]]]]]]]],
			else:
				print depth2
			if len(rule) > 0:
				fw['rules'].append(rule)
		fws.append(fw)
	
	logger.debug(json.dumps(fws, indent=4))
		
	
	return fws
	
def update_firewall_task(fwname, fwinfo):
	commands = []
	
	rule_num = fwinfo['rule']
	
	# 이전 ethernet 삭제
	if 'ethernet' in fwinfo and len(fwinfo['ethernet']) > 0:
		if 'before_eth' in fwinfo:
			commands.append("$DELETE interfaces ethernet %s firewall" % fwinfo['before_eth'])
	
	for key in fwinfo:
		if '_' in key:
			_key = key.replace('_',' ')
		else:
			_key = key
			
		if key == 'before_eths':
			continue # 앞에서 처리했음으로.. pass.
		
			
			
		if key == 'ethernet':
			for eth in fwinfo[key]:
				commands.append("$SET interfaces ethernet %s firewall %s %s" % (eth, fwinfo['inout'], fwname))
		else:
			commands.append("$DELETE firewall name %s rule %s %s" % (fwname, rule_num, _key))
			if len(fwinfo[key]) > 0:
				#값이 있을때만 set 
				commands.append("$SET firewall name %s rule %s %s %s" % (fwname, rule_num, _key, fwinfo[key]))
				
	return FabricUtilNFV.send_vyatta_command(commands)
	
def update_firewall(vmid, params):
	
	diff = PyUtils.diff_vyatta_conf(params['before'], params['after'])
	
	diff['rule'] = params['before']['rule'] # rule number
	diff['before_eth'] = params['before']['ethernet']
	
	if len(diff) == 0:
		logger.debug("firewall 수정사항이 없습니다.")
		return {"success": "fail", "errmsg": "수정 사항이 없습니다."}
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(update_firewall_task, hosts=[addr], fwname=params['name'], fwinfo = diff)
	
	return results[addr]
	
def delete_firewall_task(fwinfo):
	fwname = fwinfo['name']
	commands = []
	
	if 'ethernet' in fwinfo and len(fwinfo['ethernet']) > 0:
		commands.append("$DELETE interfaces ethernet %s firewall" % fwinfo['ethernet'])
	
	commands.append("$DELETE firewall name %s rule %s " % (fwname, fwinfo['rule']))
		
	return FabricUtilNFV.send_vyatta_command(commands)
	
def delete_firewall(vmid, params):
	
	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(delete_firewall_task, hosts=[addr], fwinfo = params)

	return results[addr]