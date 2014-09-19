'''
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, env
from fabric.tasks import execute
import rpyc
import json

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
	result = run('configure', pty=False)
	result = run('show interfaces', pty=False)
	lines = result.split('\n')
	conn = rpyc.connect("centos7", 18881)
	conn.root.add_pattern('VYATTA_ETH_STATUS', '[uDA]')
	foundHeader = False
	for line in lines:
		print "LINE: " + line
		if conn.root.parse(line, r"Interface%{SPACE}IP Address%{SPACE}S/L  Description"):
			foundHeader = True
		
		if foundHeader:
			parsed = conn.root.parse(line, r"%{USERNAME:nic_name}%{SPACE:}%{IP:addr}/%{NUMBER:subnet}%{SPACE:}%{VYATTA_ETH_STATUS:state}/%{VYATTA_ETH_STATUS:link}")
			if parsed != None:
				print parsed

def locale():
	run('locale')

if __name__ == "__main__":
	execute(dev)
# 	execute(locale)
	execute(show_interfaces, hosts=['vyatta'])
