#-*- coding: utf-8 -*-
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
			nic[attr[0]] = attr[1]
		
		if filter == None:
			nics.append(nic)
		elif filter == eth[0]:
			nics.append(nic)
			
	return nics

def getInterfaces(addr, sshid, sshpw, pfilter):
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
	
	services =[]
	for svc in results.asList():
		print svc
		service = {'service': svc[0]}
		
		for attr in svc[1]:
			if len(attr) > 2:
				service[attr[0]] = [attr[1], attr[2]]
			elif len(attr) > 1:
				service[attr[0]] = attr[1]
			else:
				service[attr[0]] = True
		
		services.append(service)
	
	return services

def getServices(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_service_with_configure, hosts=[addr])
	return results[addr]

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
	nicinfo = {}
	result = run('/sbin/ifconfig -a ' + nicname, pty=False, quiet=True)
	lines = result.split('\n')
	for line in lines:
 		print "LINE: " + line
 		if "inet addr" in line:
 			ipAddr = line.split()[1].split(':')[1]
#			subnet = line.split()[3].split(':')[1]
 			nicinfo['ipaddr'] = ipAddr
# 			nic['subnet'] = subnet
	return nicinfo

def getIfConfig(addr, sshid, sshpw, nicname):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(ifconfig_task, hosts=[addr], nicname=nicname)
	return results[addr]

def send_vyatta_command(commands):
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

def update_nic_task(beforeData, afterData):
	options = {
		"duplex": "duplex",
		"smp_affinity": "smp_affinity",
		"hw-id": "hw_id",
		"speed": "speed",
		"address": "address"
	}

	commands = []
	results = []
	ethName = afterData["ethName"]
	for key in afterData:
		beforeValue = beforeData[key]
		afterValue = afterData[key]
		
		if beforeValue != afterValue:
			commands.append("$SET interfaces ethernet %s %s %s" % (ethName, options[key], afterValue))
			if key == "address" or key == "hw-id":
				diff = {"ethName": ethName, key: afterValue}
				results.append(diff)

	# replace below code to send_vyatta_command(commands) ??
	f = open(mainDir + '/commands.txt', 'w')
	commands.append("$COMMIT")
	commands.append("$SAVE")
	logger.debug(commands)
	f.write("\n".join(commands))
	f.close()

	run('mkdir -p .spider')
	with cd('.spider'):
		put(open(mainDir + '/cli.txt'), 'cli.sh', mode=0755)
		put(open(mainDir + '/commands.txt'), 'commands.sh', mode=0755)
		try:
			result = run('./cli.sh', pty=False, combine_stderr=True)
			logger.debug("--------------------------------")
			logger.debug("Run result %s" % result)
			logger.debug("--------------------------------")
		except Exception, e:
			return result, 500
	if "Commit failed" in result: 
		logger.debug("fail", errmsg = result)
		return result, 500
	else:
		logger.debug("success")
		return results

def update_nic(addr, sshid, sshpw, jsonData):
    env.hosts = [ addr ]
    env.user = sshid
    env.password = sshpw
    env.shell = '/bin/vbash -ic'
    results = execute(update_nic_task, hosts=[addr], beforeData = jsonData['before'], afterData=jsonData['after'])
    return results[addr]

