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
Created on 2014. 11. 11.

Vyatta HTTPS, SSH Service 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV

logger = logging.getLogger(__name__)

def get_remote_service(vmid):
    logger.debug("get_remote_service call!!")
    
    vm = get_vm(vmid)
    
    results = []
    services = FabricUtilNFV.getServices(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for service in services:
        if service['service'] == 'ssh' or service['service'] == 'https':
            results.append(service)

    return results

def update_remote_service_task(serviceinfo):
    if 'httpsenable' in serviceinfo:
        httpsenable = serviceinfo['httpsenable']
    else:
        httpsenable = None
    
    if 'httpsaddr' in serviceinfo:
        httpsaddr = serviceinfo['httpsaddr']
    else:
        httpsaddr = None
    
    if 'sshenable' in serviceinfo:
        sshenable = serviceinfo['sshenable']
    else:
        sshenable = None
    
    if 'allowroot' in serviceinfo:
        allowroot = serviceinfo['allowroot']
    else:
        allowroot = None
    
    if 'sshaddr' in serviceinfo:
        sshaddr = serviceinfo['sshaddr']
    else:
        sshaddr = None
    
    if 'sshport' in serviceinfo:
        sshport = serviceinfo['sshport']
    else:
        sshport = None
        
    commands = []
    
    if httpsenable and httpsenable == 'true':
        commands.append("$SET service https")
        commands.append("$DELETE service https listen-address")
        
        addrs = httpsaddr.split(',')
        
        for addr in addrs:
            commands.append("$SET service https listen-address " + addr)
    else:
        commands.append("$DELETE service https")
        
    '''
    # SSH 관련 기능은 관리상의 이슈로 현재는 읽기 전용으로만 제공
    if sshenable and sshenable == 'true':
        commands.append("$DELETE service ssh listen-address")
        
        if allowroot and allowroot == 'true':
            commands.append("$SET service ssh allow-root")
        else:
            commands.append("$DELETE service ssh allow-root")
        
        if sshport:
            commands.append("$SET service ssh port " + sshport)
        
        addrs = sshaddr.split(',')
        
        for addr in addrs:
            commands.append("$SET service ssh listen-address " + addr)
    '''
        
    return FabricUtilNFV.send_vyatta_command(commands)

def update_remote_service(vmid, params):
    logger.debug("update_remote_service call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(update_remote_service_task, hosts=[addr], serviceinfo = params)

    return results[addr]