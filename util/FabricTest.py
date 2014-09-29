'''
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, env, put, cd
from fabric.tasks import execute
import rpyc
import json
from pyparsing import *

keywords = CaselessKeyword('interfaces') | CaselessKeyword('nat') | CaselessKeyword('service') | CaselessKeyword('system')
elementList = Forward()
string = Word( alphanums+'_-:/.+@$' )
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                   Optional( '.' + Word(nums) ) +
                   Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
value = string | number | dblQuotedString.setParseAction(removeQuotes)
unaryItem = value + lineEnd()
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


def dev():
	env.hosts = [ 'vyatta' ]
	env.user = 'vyatta'
	env.password = 'vyatta'
	env.shell = '/bin/vbash -ic'

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
	f = open('./commands.txt', 'w')
	commands = [
# 			'$SET interfaces loopback lo address 127.0.0.5/24',
# 			'$COMMIT',
			'$SHOW interfaces'
			]
	f.write("; ".join(commands))
	f.close()
	with cd('/home/vyatta/test/scripts'):
		put('./cli.txt', 'cli.sh', mode=0755)
		put('./commands.txt', 'commands.sh', mode=0755)
		result = run('./cli.sh', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	import pprint
	results = elementList.parseString(result)
#  	pprint.pprint( results.asList() )
 	
 	for eth in results.asList():
 		print "---------------------------------"
#  		pprint.pprint(eth)
 		ethName = eth[1]
 		print "ethName: " + ethName
 		
 		for attr in eth[2]:
 			key = attr[0]
 			val = attr[1]
 			print "  %s: %s" % (key, val)
 			
 		
 	


def locale():
	run('locale')

if __name__ == "__main__":
	execute(dev)
# 	execute(locale)
	execute(show_interfaces_with_configure, hosts=['vyatta'])
