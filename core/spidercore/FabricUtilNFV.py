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
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, env, put, cd
from fabric.tasks import execute
import rpyc
import json
from spidercore import *
from __builtin__ import int
import os
import tempfile

logger = logging.getLogger(__name__)

def show_interfaces():
	result = run('show interfaces', pty=False, quiet=True)
	lines = result.split('\n')
	try :
		conn = rpyc.connect("centos7", 18881)
	except:
		print "You may not run python GrokService.py at centos7. Please check it"
		exit(1)
	conn.root.add_pattern('VYATTA_ETH_STATUS', '[uDA]')
	foundHeader = False
	for line in lines:
# 		print "LINE: " + line
		if conn.root.parse(line, r"Interface%{SPACE}IP Address%{SPACE}S/L  Description"):
			foundHeader = True
		
		if foundHeader:
			parsed = conn.root.parse(line, r"%{USERNAME:nic_name}%{SPACE:}%{IP:addr}/%{NUMBER:subnet}%{SPACE:}%{VYATTA_ETH_STATUS:state}/%{VYATTA_ETH_STATUS:link}")
			if parsed != None:
				print parsed

def show_interfaces_with_configure(filter):
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW interfaces'
			]
	f.write("; ".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False, quiet=True)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	nics =[]
	for eth in results.asList():
		
		nic = {'ethName': eth[1]}
		
		for attr in eth[2]:
			if len(attr) == 1:
				nic[attr[0]] = True
			elif 'firewall' == attr[0]:
				nic[attr[0]] = [attr[1][0][0], attr[1][0][1][0][1]] #"firewall": [["in", [["name", "test-firewall2"]]]]
			else:
				nic[attr[0]] = attr[1]
		
		if filter == None:
			if eth[0] == 'loopback':
				continue
			nics.append(nic)
		elif filter == 'all':
			nics.append(nic)
		elif filter.startswith("!") and filter[1:] == eth[0]:
			continue # exclude
		elif filter == eth[0]:
			nics.append(nic)
			
	return nics

def getInterfaces(addr, sshid, sshpw, pfilter):
	'''
		show interfaces 결과 가져오기
		@param: pfilter는 [None|bonding|ethernet|loopback|all] 중 하나를 줄수있다.
			- None 는 기본적으로 loopback 을 제외하고 가져온다.
			- all 은 모든 interfaces 를 가져온다.
	'''
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_interfaces_with_configure, hosts=[addr], filter = pfilter)
	return results[addr]

def show_nat_with_configure():
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW nat'
			]
	f.write("; ".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	rules =[]
	for srctgt in results.asList():
		if len(srctgt[1]) > 0:
			for ruleAry in srctgt[1]:
				#print "ruleAry :", ruleAry
				ruleNum = ruleAry[1]
				
				rule = {'rule': ruleNum}
				rule['isSource'] = (srctgt[0].lower() == 'source')
				
				for attr in ruleAry[2]:
					if len(attr) == 1:
						rule[attr[0]] = True
					else:
						if type(attr[1]) == list:
							temp = {}
							for prop in attr[1]:
								temp[prop[0]] = prop[1]
							rule[attr[0]] = temp
						else:
							rule[attr[0]] = attr[1]
					
				#print "rule :", rule
				rules.append(rule)

	return rules

def getNATs(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_nat_with_configure, hosts=[addr])
	return results[addr]

def show_service_with_configure():
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW service'
			]
	f.write("; ".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	services = []
	for svc in results.asList():		
		service = parseElements(svc[1])
		service['service'] = svc[0]
		services.append(service)
	
	return services

def getServices(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_service_with_configure, hosts=[addr])
	return results[addr]

def show_protocols_with_configure():
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW protocols'
			]
	f.write("; ".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	protocols = []
	for item in results.asList():		
		protocol = parseElements(item[1])
		protocol['protocol'] = item[0]
		protocols.append(protocol)
	
	return protocols

def getProtocols(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_protocols_with_configure, hosts=[addr])
	return results[addr]

def show_system_with_configure():
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW system'
			]
	f.write("; ".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
	pprint.pprint( results.asList() )
	
	protocols = []
	for item in results.asList():
		if type(item[1]) == list:
			protocol = parseElements(item[1])
			protocol['category'] = item[0]
		else:
			protocol = {item[0]:item[1]}
			protocol['category'] = item[0]
			
		protocols.append(protocol)
	
	return protocols

def getSystem(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_system_with_configure, hosts=[addr])
	return results[addr]

def parseElements(attr):
	result = {}
	
	if type(attr) == list:
		for prop in attr:
			if len(prop) == 1:
				result[prop[0]] = True
			elif len(prop) == 2:
				if type(prop[1]) == list:
					result[prop[0]] = parseElements(prop[1])
				else:
					if prop[0] in result:
						result[prop[0]] = result[prop[0]] + "," + prop[1]
					else:
						result[prop[0]] = prop[1]
			else:
				temp = parseElements(prop[2])
				temp['key_name'] = prop[1]
				
				if prop[0] not in result:
					result[prop[0]] = []

				result[prop[0]].append(temp)
	
	return result

def assignIdToCollectD(vmId):
	#	Uncomment Hostname and assign vmhostId as Hostname to /etc/collectd/collectd.conf
	#	@@FIXME: Fabric itself has an interface(api) to handle remote file directly like sed !!
	f = open(mainDir + '/sed.txt', 'w')
	commands = [
			'cd /etc/collectd\n'
			'sed -e "s/#Hostname\s\\".*\\"/Hostname \\"' + vmId +'\\"/" collectd.conf > c.conf\n'
			'cat c.conf | grep Hostname\n'
			'cp c.conf collectd.conf\n'
			'service collectd restart'
			]
	f.write("; ".join(commands))
	f.close()
	#	Remote sciprt will be stored in "~/.spider" directory
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/sed.txt'), 'sed.sh', mode=0755)
		result = sudo('./sed.sh', pty=False, quiet=True)

	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	return

def renameHostname(hostname):
	f = open(mainDir + '/commands.txt', 'w')
	commands = [
			"$SET system host-name %s" % hostname,
			'$COMMIT',
			'$SAVE'
			]
	f.write("\n".join(commands))
	f.close()
	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	return

def initVM(addr, sshid, sshpw, id, vmhostName):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(assignIdToCollectD, hosts=[addr], vmId = id)

	env.shell = '/bin/vbash -ic'
	results = execute(renameHostname, hosts=[addr], hostname = vmhostName)
	return

def pingVM_task():
	try:
		succeeded = run('ls', pty=False, quiet=True).succeeded and sudo('id', pty=False, quiet=True).succeeded
	except Exception, e:
		succeeded = False
	return succeeded

def pingVM(addr, sshid, sshpw):
	os.system("rm ~/.ssh/known_hosts")
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(pingVM_task, hosts=[addr])
	return results[addr]


def ifconfig_task(nicname):
	ifconfig = {}
	ethName = ""
	ipAddr = ""
	#nicinfo = {}
	#result = run('/sbin/ifconfig -a ' + nicname, pty=False, quiet=True)
	result = run('/sbin/ifconfig -a', pty=False, quiet=True)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line
		if "Link encap" in line:
			ethName = line.split()[0]
		if "inet addr" in line:
			ipAddr = line.split()[1].split(':')[1]
#			subnet = line.split()[3].split(':')[1]
			#nicinfo['ipaddr'] = ipAddr
# 			nic['subnet'] = subnet
		if len(line) == 0:
			ifconfig[ethName] = ipAddr
			ethName = ""
			ipAddr = ""
	return ifconfig

def getIfConfig(addr, sshid, sshpw, nicname):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(ifconfig_task, hosts=[addr], nicname=nicname)
	return results[addr]

def send_vyatta_command(commands):
	# Remove known_hosts file to prevent host key verification failed.
	os.system("rm ~/.ssh/known_hosts")
	
	results = []
	tempDir = mainDir+"/tmp"
	#f = open(mainDir + '/commands.txt', 'w')
	# 임시파일 생성해서 사용
	f = tempfile.NamedTemporaryFile(mode='w+b', delete=False, dir=tempDir, suffix=".sh")
	commands.insert(0, ". ./env.sh")
	commands.append("$COMMIT")
	commands.append("$SAVE")
	
	cmdStr = "\n".join(commands);
	logger.debug("commands: \n" + cmdStr)
	
	f.write(cmdStr)
	f.close()
	
	filename = os.path.basename(f.name)

	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/env.txt'), 'env.sh', mode=0755)
		put(open(f.name), filename, mode=0755)
		try:
			result = run("./" + filename, pty=False, combine_stderr=True)
			logger.debug("--------------------------------")
			logger.debug("Run result %s" % result)
			logger.debug("--------------------------------")
		except Exception, e:
			return {"success": "fail", "errmsg": result}
		finally:
			# 실행 완료된 파일을 제거한다.
			run('rm -f ' + filename)
			os.remove(f.name)
		
	# see Case 420 
	for item in ['already exists','Commit failed','failed']:
		
		if item in result:
			logger.error("vyatta command fail.")
			return {"success": "fail", "errmsg": result}
	else:
		logger.debug("success")
		return {"success": "success", "msg": result}


def get_vyatta_conf_task(command):
	if type(command) == list:
		return send_vyatta_command(command)
	else:
		return send_vyatta_command([command])



def get_vyatta_conf(vmid, pcommand):
	""" vyatta 설정 정보(string) 가져오기
	
		@param: vmid:   vm id.
		@param: pcommand:  show 로 시작하는 vyatta command
		
		@return: vyatta 설정 정보(string)
	"""

	vm = get_vm(vmid)
	addr = vm['mgraddr']
	
	env.hosts = [ addr ]
	env.user = vm['sshid']
	env.password = vm['sshpw']
	env.shell = '/bin/vbash -ic'
	results = execute(get_vyatta_conf_task, hosts=[addr], command=pcommand)
	
	#앞뒤 2줄씩 삭제하고 리턴
	_list = results[addr]['msg'].split('\n')
	return "\n".join(_list[2: len(_list)-2])

def get_all_nic_config(vmid):
	
	configs = {}
	configList = []
	logs = get_vyatta_conf(vmid, "$SHOW interfaces")
	for line in logs.split("\n"):
		if "{" in line:
			ethName = line.split()[1]
		elif "}" in line:
			configs[ethName] = "\n".join(configList)
			configList = []
		else:
			configList.append(line)
	
	return configs

def refresh_vm_task():
	try:
		succeeded = sudo('/etc/spider/init.sh', pty=False, quiet=True).succeeded
	except:
		succeeded = False
		
	return succeeded

def refresh_vm(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	
	results = execute(refresh_vm_task, hosts=[addr])
	
	return results[addr]