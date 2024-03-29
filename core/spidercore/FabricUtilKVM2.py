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
Created on 2014. 10. 15.

@author: mwchoi
'''

from fabric.api import run, sudo, env, put, cd
from fabric.tasks import execute
import re
import json
import paramiko, time
import select
from spidercore import *



### vm list ###
def virsh_list_all():
	result = run('virsh list --all', pty=False, quiet=True)
	lines = result.split('\n')
	vms = []
	for line in lines[2:]:
		print "LINE: " + line
		words = line.strip().split()
		if (len(words)==4):
			vms.append({'id': words[0], 'name': words[1], 'state': words[2]+ ' ' + words[3]})
		else:
			vms.append({'id': words[0], 'name': words[1], 'state': words[2]})
	return vms

def getDomainList(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(virsh_list_all, hosts=[addr])
	return results[addr]





### vm template list ###
def templatelist():
	result = run('virsh list --all | grep template', pty=False, quiet=True)
	lines = result.split('\n')
	vms = []
	for line in lines[:]:
		print "LINE: " + line
		words = line.strip().split()
		if (len(words)==4):
			vms.append({'id': words[0], 'name': words[1], 'state': words[2]+ ' ' + words[3]})
		else:
			vms.append({'id': words[0], 'name': words[1], 'state': words[2]})
			
	return vms


def getTemplatelist(addr, sshid, sshpw):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	try:
		results = execute(templatelist, hosts=[addr])
	except EOFError:  #접속 에러..
		return []
	
	return results[addr]




### domain info ###
def dominfo(command_):
	
	results = run('virsh dominfo ' + command_ , pty=True ,quiet=True,  timeout=5 )
	vminfo = []

	for line in results.split('\n'):
		line = line.strip()
		key, value = line.split(':')
		vminfo.append({key.lower().strip():value.strip()})

	return vminfo

def getDominfo(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(dominfo, name, hosts=[addr])
	
	return results[addr]



### domstate ###
def domstate(command_):

	results = run('virsh domstate ' + command_ , pty=True ,quiet=True,  timeout=5 )
	vms = []
	vms.append({'state':results})
	
	return vms
	


def getDomstate(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(domstate, name, hosts=[addr])
	
	return results[addr]


def vm_all_state_task(vmList):

	logs = run('virsh list --all' , pty=True ,quiet=True,  timeout=5 )
	
	result = []
	
	for line in logs.split("\n")[2:]:
		tokens = line.split()
		if tokens[1] in vmList["vms"]:
			stat = {}
			if vmList[tokens[1]]:
				stat[tokens[1]] = "interim"
			else:
				stat[tokens[1]] = "".join(tokens[2:])
			result.append( stat )
	
	return result
	


def getVmAllState(addr, sshid, sshpw, vms):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(vm_all_state_task, hosts=[addr], vmList = vms)
	
	return results[addr]


### domstart ###

def domstart(command_):

	_result = ''
	results = run('virsh start ' + command_ , pty=True ,quiet=True,  timeout=5 )
	
	print results
	
	matchStr = "error"
	
	_result = re.search(matchStr,results)

	vms = []	

	if _result:
		lines = results.split('\n')
		vms = []
		for line in lines[:]:
			print "LINE: " + line
			words = line.strip().split(':')
			vms.append({words[0] : words[1]})
				
		return vms

	else:
		vms.append({'state':results})
		return vms



	
	

def getDomstart(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(domstart, name, hosts=[addr])
	
	return results[addr]


### domshutdown ###

def domshutdown(command_):

	results = run('virsh shutdown ' + command_ , pty=True ,quiet=True,  timeout=5 )

	print results

	_result = ''
	matchStr = "error"
	
	_result = re.search("(" + matchStr + ".*)" , results)
	
	vms = []	

	if _result:
		lines = results.split('\n')
		vms = []
		for line in lines[:]:
			print "LINE: " + line
			words = line.strip().split(':')
			vms.append({words[0] : words[1]})
				
		return vms

	else:
		vms.append({'state':results})
		return vms
	


def getDomshutdown(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(domshutdown, name, hosts=[addr])
	
	return results[addr]



### domdefine ###

def domdefine(command_):

	results = run('virsh define /etc/libvirt/qemu/' + command_ + '.xml', pty=True ,quiet=True,  timeout=5 )
	print results

	vms = []
	vms.append({'state':results})
	
	return vms


def getDomdefine(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(domdefine, name, hosts=[addr])
	
	return results[addr]



### dom undefine ###

def domundefine(command_):

	results = run('virsh undefine ' + command_ , pty=True ,quiet=True,  timeout=5 )
	vms = []
	vms.append({'state':results})
	
	return vms


def getDomundefine(addr, sshid, sshpw, name):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(domundefine, name, hosts=[addr])
	
	return results[addr]



### dom clone ###

def domclone(command_):

	template = command_[0]
	newvm = command_[1]

	results = run('mkdir -p /data/libvirt/logs && virt-clone -o ' + template + ' -n ' + newvm + ' -f /data/libvirt/images/' + newvm + '.img > /data/libvirt/logs/' + newvm + '.log' , 
				pty=True ,quiet=True,  timeout=None )
	vms = []
	vms.append({'state':results})
	
	return vms


def getDomclone(addr, sshid, sshpw, template, newvm):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	args = []
	args.append(template)
	args.append(newvm)
	
	results = execute(domclone, args , hosts=[addr])
	
	return results[addr]



def getDomcloneParamiko(addr, sshid, sshpw, template, newvm):

	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	args = []
	args.append(template)
	args.append(newvm)
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
	ssh.connect(addr, username=sshid, password=sshpw)
	
	results = ''
	rl = ''
	wl = ''
	xl = ''

	# Send the command (non-blocking)
	stdin, stdout, stderr = ssh.exec_command('mkdir -p /data/libvirt/logs && virt-clone -o ' + template + ' -n ' + newvm + ' -f /data/libvirt/images/' + newvm + '.img > /data/libvirt/logs/' + newvm + '.log')
	
	
	# Wait for the command to terminate
	while not stdout.channel.exit_status_ready():
		# Only print data if there is data to read in the channel
		if stdout.channel.recv_ready():
			rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
			if len(rl) > 0:
				# Print data from stdout
				print stdout.channel.recv(1024),

	
	#
	# Disconnect from the host
	#
	print "Command done, closing SSH connection"
	ssh.close()

	






### dom clone ###

def domremove(command_):

	results = run('rm -f  /data/libvirt/images/' + command_ + '.img ' , 
				pty=True ,quiet=True,  timeout=None )
	vms = []
	vms.append({'state':results})
	
	return vms


def getDomremove(addr, sshid, sshpw, delvm):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'

	'''
	try:
	     results = execute(domshutdown, newvm , hosts=[addr])
	     
	except IOError, e:
	     print e
	print results
	'''
	results = execute(domundefine, delvm , hosts=[addr])
	print results
	
	results = execute(domremove, delvm , hosts=[addr])
	print results
	
	return results[addr]








def virsh_getAllInfo():
	try:
		result = run('virsh nodeinfo', pty=False, quiet=True)
		
		'''
		<In case of error message>
		sudo: sorry, you must have a tty to run sudo
		command not found
		error: failed to connect to the hypervisor
		error: no valid connection
		error: internal error: Unable to locate libvirtd daemon in /usr/sbin (to override, set $LIBVIRTD_PATH to the name of the libvirtd binary)
		'''
		
		if 'sudo:' in result and 'command not found' in result or 'error:' in result:
			raise Exception("Not a vm host")
	except:
		return {'msg':'Not a vm host or network is unreachable.'}

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
	try:
		env.hosts = [ addr ]
		env.user = sshid
		env.password = sshpw
		env.shell = '/bin/bash -l -c'
		results = execute(virsh_getAllInfo, hosts=[addr])
		return results[addr]
	except:
		return {"msg":"Unhandled Exception has occurred."}


def clonestate(vmname):
	ps_result = run('ps -ef | grep virt-clone | grep ' + vmname + ' | grep -v grep', pty=False, quiet=True)
	
	print 'ps -ef | grep virt-clone | grep ' + vmname + ' | grep -v grep => ' + ps_result
	
	if ps_result == "":
		# no running process to vm clone
		cat_result = run('cat /data/libvirt/logs/' + vmname + '.log | grep "created successfully."', pty=False, quiet=True)
	
		print 'cat /data/libvirt/logs/' + vmname + '.log | grep "created successfully." => ' + cat_result
		
		if cat_result == "":
			state = "error"
		else:
			# in case of file does not exist or has "created successfully." string in file.
			state = "success"
	else:
		# vm clone is running 
		state = "cloning"
	
	return state

def getClonestate(addr, sshid, sshpw, vmname):
	env.hosts = [ addr ]
	env.user = sshid
	env.password = sshpw
	env.shell = '/bin/bash -l -c'
	results = execute(clonestate, hosts=[addr], vmname = vmname)
	return results[addr]
	

if __name__ == "__main__":


	jsonData = {'vmhost':'e851525e-be30-4914-92ec-00ab5be7de26','name':'spidervm3'}
	vmHostId = jsonData['vmhost']
	name = jsonData['name']


	newvm = 'newvm'
	template = 'template_02'


# 	Finding a VM Host designated in the JSON request
	vmhosts = read_repository("vmhosts")
	found = False
	for vmhost in vmhosts:
		if vmhost['_id'] == vmHostId:
			jsonData['vmhostname'] = vmhost['name']


			############   Domain List All
#			vms = getDomainList(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'])
#			print vms			
			

			############   Template List All
			#vms = getTemplatelist(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'])
			#print vms					
			
			############   Domain info
			vms = getDominfo(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
			print vms			


			############   Domain state
			#vms = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
			#print vms

			############   Domain start
			#vms = getDomstart(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
			#print vms

			############   Domain shutdown
#			vms = getDomshutdown(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
#			print vms

			############   Domain undefine
#			vms = getDomundefine(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
#			print vms

			############   Domain define
#			vms = getDomdefine(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],name)
#			print vms

			############   Domain clone
#			vms = getDomcloneParamiko(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], template, newvm)
#			print vms

			############   Domain remove
#			vms = getDomremove(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'], newvm)
#			print vms


			############   Domain state
#			vms = getDomstate(vmhost['addr'], vmhost['sshid'], vmhost['sshpw'],newvm)
#			print vms

			
			
			found = True
	

    
