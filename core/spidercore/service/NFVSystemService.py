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
Created on 2014. 11. 18.

Vyatta System Service 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV

logger = logging.getLogger(__name__)

def get_system(vmid):
    logger.debug("get_system call!!")
    
    vm = get_vm(vmid)
    
    results = []
    system = FabricUtilNFV.getSystem(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for prop in system:
        if prop['category'] == 'host-name' or prop['category'] == 'time-zone' or prop['category'] == 'login':
            results.append(prop)

    return results

def set_global_system_task(systeminfo):
    if 'hostname' in systeminfo:
        hostname = systeminfo['hostname']
    else:
        hostname = None
    
    if 'timezone' in systeminfo:
        timezone = systeminfo['timezone']
    else:
        timezone = None
        
    commands = []
    
    if hostname:
        commands.append("$SET system host-name " + hostname)
    
    if timezone:
        commands.append("$SET system time-zone " + timezone)
        
    return FabricUtilNFV.send_vyatta_command(commands)
        
def set_global_system(vmid, params):
    logger.debug("set_global_system call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(set_global_system_task, hosts=[addr], systeminfo = params)

    return results[addr]

def set_login_user_task(userinfo):
    if 'username' in userinfo:
        username = userinfo['username']
    else:
        username = None
    
    if 'level' in userinfo:
        level = userinfo['level']
    else:
        level = None
    
    if 'password' in userinfo:
        password = userinfo['password']
    else:
        password = None
    
    if 'key_id' in userinfo:
        key_id = userinfo['key_id']
    else:
        key_id = None
    
    if 'key_type' in userinfo:
        key_type = userinfo['key_type']
    else:
        key_type = None
    
    if 'key_value' in userinfo:
        key_value = userinfo['key_value']
    else:
        key_value = None
        
    commands = []
    
    if username:
        if level:
            commands.append("$SET system login user " + username + " level " + level)
        else:
            commands.append("$SET system login user " + username)
            
        if password:
            commands.append("$SET system login user " + username + " authentication plaintext‐password " + password)
        
        if key_id and key_type and key_value:
            commands.append("$SET system login user " + username + " authentication public-keys " + key_id + " type " + key_type)
            commands.append("$SET system login user " + username + " authentication public-keys " + key_id + " key " + key_value)
        
    return FabricUtilNFV.send_vyatta_command(commands)

def set_login_user(vmid, params):
    logger.debug("set_login_user call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(set_login_user_task, hosts=[addr], userinfo = params)

    return results[addr]