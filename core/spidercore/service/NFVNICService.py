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
	
	
	Created on 2014. 11. 11.
	@author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV
from spidercore.util import PyUtils

logger = logging.getLogger(__name__)


def update_nic_task(ethName, diff):
	'''
	options = {
		"duplex": "duplex",
		"smp_affinity": "smp_affinity",
		"hw-id": "hw_id",
		"speed": "speed",
		"address": "address"
	}
	'''

	commands = []
	
	for key in diff:
		
		if key == "disable" and diff[key] == "false":
			diff[key] = '' # delete 만 하기 위해.
			
		
		if '_' in key:
			_key = key.replace('_',' ')
		else:
			_key = key
			
		# 무조건 삭제후
		commands.append("$DELETE interfaces ethernet %s %s" % (ethName, key))
		if len(diff[key]) > 0:
			if key == "disable" and diff[key] == "true":
				commands.append("$SET interfaces ethernet %s %s" % (ethName, key))
			else:
				#값이 있을때만 set 
				commands.append("$SET interfaces ethernet %s %s %s" % (ethName, key, diff[key]))
				

	return FabricUtilNFV.send_vyatta_command(commands)

def update_nic(vmid, params):
	
	pdiff = PyUtils.diff_vyatta_conf(params['before'], params['after'])
	
	if len(pdiff) == 0:
		logger.debug("NIC 수정사항이 없습니다.")
		return {"success": "success", "msg": "수정 사항이 없습니다."}
	
	vms = read_repository("vms")
	
	for vm in vms:
		print vm['_id'] + " : " + vmid
		if '_id' in vm and vmid == vm['_id']:
			break
	if vm == None:
		raise ValueError("get_vm not found: " + vmid)

	pEthName = params['after']['ethName']
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(update_nic_task, hosts=[addr], ethName = pEthName, diff=pdiff)
	
	
	# vms.json 파일도 변경해주기.
	modified = False
	for key in pdiff:
		if "hw-id" == key:
			vm["interfaces"][pEthName]["macaddr"] = pdiff[key]
			modified = True
		elif "address" == key:
			modified = True
			if pdiff[key] == "dhcp":
				nicinfo = FabricUtilNFV.getIfConfig(addr, vm['sshid'], vm['sshpw'], pEthName)
				vm["interfaces"][pEthName]["ipaddr"] = nicinfo['ipaddr']
			else:
				vm["interfaces"][pEthName]["ipaddr"] = pdiff[key]
	
	if modified:
		write_repository('vms', vms)
	
	return results[addr]