# ########################## Copyrights and license ############################################
#                                                                                              #
# Copyright 2014 Open Source Consulting, Inc. <support@osci.kr>                                #
#                                                                                              #
# This file is part of athena-spider. https://github.com/OpenSourceConsulting/athena-spider    #
#                                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under                    #
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
import json
from spidercore import *



def virsh_list_all():
	result = run('virsh list --all', pty=False, quiet=True)
	lines = result.split('\n')
	vms = []
	for line in lines[2:]:
		print "LINE: " + line
		words = line.strip().split()
		vms.append({'id': words[0], 'name': words[1], 'state': words[2]})

	return vms

def getDomainList(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(virsh_list_all, hosts=[addr])
	return results[addr]

def virsh_getAllInfo():
	result = run('virsh nodeinfo', pty=False, quiet=True)
	lines = result.split('\n')
	info = []
	for line in lines:
		print "LINE: " + line
		words = line.split(':')
		info.append({'name': words[0].strip(), 'value': words[1].strip()})

	result = run('virsh version', pty=False, quiet=True)
	lines = result.split('\n')
	version = []
	for line in lines:
		print "LINE: " + line
		words = line.split(':')
		version.append({'name': words[0].strip(), 'value': words[1].strip()})

	result = run('virsh hostname', pty=False, quiet=True)
	hostname = result.strip()

	result = run('virsh iface-list', pty=False, quiet=True)
	lines = result.split('\n')
	interfaces = []
	for line in lines[2:]:
		print "LINE: " + line
		words = line.strip().split()
		interfaces.append({'name': words[0], 'state': words[1], 'macaddr': words[2]})

	return {'info': info, 'version': version, 'hostname': hostname, 'interfaces': interfaces}

def getAllInfo(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(virsh_getAllInfo, hosts=[addr])
	return results[addr]


def virsh_get_macaddrs_from_all_domains():
	result = run('virsh list --all', pty=False, quiet=True)
	lines = result.split('\n')
	vms = []
	for line in lines[2:]:
		print "LINE: " + line
		domain = line.strip().split()[1]

		result = run("virsh domiflist %s" % domain, pty=False, quiet=True)
		nics = result.split('\n')
		vm = {'domain': domain, 'macaddrs': []}
		for nic in nics[2:]:
			macaddr = nic.split()[4]
			vm['macaddrs'].append(macaddr)
		
		vms.append(vm)

	return vms

def getAllMacAddrs(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(virsh_get_macaddrs_from_all_domains, hosts=[addr])
	return results[addr]


