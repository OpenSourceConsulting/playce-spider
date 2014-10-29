'''
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, env, put, cd
from fabric.tasks import execute
import rpyc
import json
from spidercore import *
from pyparsing import *
from __builtin__ import int

keywords = CaselessKeyword('interfaces') | CaselessKeyword('nat') | CaselessKeyword('service') | CaselessKeyword('system')
elementList = Forward()
string = Word( alphanums+'_-:/.+@$' )
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                   Optional( '.' + Word(nums) ) +
                   Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
value = string | number | dblQuotedString.setParseAction(removeQuotes)
unaryItem = Group(value + Suppress(lineEnd()))
item = Group(string + value + Suppress(lineEnd()))
element = Forward()
itemOrElement = item | unaryItem | element
element << Group(string + Optional(string) + Group(Suppress('{') + ZeroOrMore(itemOrElement) + Suppress('}')))
elementList = ZeroOrMore(itemOrElement)
rootKeywords = keywords + Group( Suppress('{') + elementList + Suppress('}'))
config = OneOrMore(rootKeywords)
vbash_message = Regex(r"vbash\:.*").setName("vbash message")
config.ignore(vbash_message)


def convertNumbers(s,l,toks):
	n = toks[0]
	try:
		return int(n)
	except ValueError, ve:
		return float(n)
	
number.setParseAction( convertNumbers )


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

def show_interfaces_with_configure():
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
#  	pprint.pprint( results.asList() )
	
	nics =[]
	for eth in results.asList():
		nic = {'ethName': eth[1]}
		
		for attr in eth[2]:
			nic[attr[0]] = attr[1]
		
		nics.append(nic)
	
	return nics

def getInterfaces(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/vbash -ic'
	results = execute(show_interfaces_with_configure, hosts=[addr])
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
		ruleAry = srctgt[1][0]
		print ruleAry
		ruleNum = ruleAry[1]
		rule = {'rule': ruleNum}
		rule['isSource'] = (srctgt[0].lower() == 'source')
		
		for attr in ruleAry[2]:
			rule[attr[0]] = attr[1]
		print rule
		
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
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(pingVM_task, hosts=[addr])
	return results[addr]


def ifconfig_task(nicname):
	result = run('/sbin/ifconfig -a ' + nicname, pty=False, quiet=True)
	return result

def getIfConfig(addr, sshid, sshpw, nicname):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(ifconfig_task, hosts=[addr], nicname=nicname)
	return results[addr]


def updateVmNIC(cmdData):

    f = open(mainDir + '/commands.txt', 'w')

    commands = [
            "$SET interfaces ethernet %s duplex %s" % (cmdData['ethName'],cmdData['duplex']),
            "$SET interfaces ethernet %s hw-id %s" % (cmdData['ethName'],cmdData['hw-id']),
            "$SET interfaces ethernet %s smp_affinity %s" % (cmdData['ethName'],cmdData['smp_affinity']),
            "$SET interfaces ethernet %s speed %s" % (cmdData['ethName'],cmdData['speed']),
            '$COMMIT',
            '$SAVE'
            ]
    print commands
    
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






def setVmNIC(addr, sshid, sshpw, jsonData):
    env.hosts = [ addr ]
    env.user = sshid
    env.password = sshpw

    env.shell = '/bin/vbash -ic'
    results = execute(updateVmNIC, hosts=[addr], cmdData = jsonData)
    return

