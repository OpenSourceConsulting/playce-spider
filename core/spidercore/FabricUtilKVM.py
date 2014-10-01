'''
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, env, put, cd
from fabric.tasks import execute
import rpyc
import json
from spidercore import *



def virsh_list_all():
	result = run('virsh list -all', pty=False)
	lines = result.split('\n')
	for line in lines:
		print "LINE: " + line

	services =[]
	
	return services

def getDomainList(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	results = execute(virsh_list_all, hosts=[addr])
	return results[addr]



