#-*- coding: utf-8 -*-
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
Created on 2014. 11. 7.

Vyatta NAT 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV

logger = logging.getLogger(__name__)

def create_nat_task(natinfo):    
    rulenum = natinfo['rulenum']
    ruletype = natinfo['ruletype']
    
    if 'ibnic' in natinfo:
        ibnic = natinfo['ibnic']
    else:
        ibnic = None
    
    if 'obnic' in natinfo:
        obnic = natinfo['obnic']
    else:
        obnic = None
    
    if 'srcaddr' in natinfo:
        srcaddr = natinfo['srcaddr']
    else:
        srcaddr = None
    
    if 'destaddr' in natinfo:
        destaddr = natinfo['destaddr']
    else:
        destaddr = None
    
    if 'srcport' in natinfo:
        srcport = natinfo['srcport']
    else:
        srcport = None
    
    if 'destport' in natinfo:
        destport = natinfo['destport']
    else:
        destport = None
    
    if 'protocol' in natinfo:
        protocol = natinfo['protocol']
    else:
        protocol = None
    
    if 'transaddr' in natinfo:
        transaddr = natinfo['transaddr']
    else:
        transaddr = None
    
    if 'transport' in natinfo:
        transport = natinfo['transport']
    else:
        transport = None
    
    if 'masquerade' in natinfo:
        masquerade = natinfo['masquerade']
    else:
        masquerade = None
    
    if 'disable' in natinfo:
        disable = natinfo['disable']
    else:
        disable = None
    
    if 'exclude' in natinfo:
        exclude = natinfo['exclude']
    else:
        exclude = None
        
    commands = []
    
    if ruletype == "destination" and ibnic:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " inbound-interface " + ibnic)
        
    if ruletype == "source" and obnic:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " outbound-interface " + obnic)
    
    if srcaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " source address " + srcaddr)
    
    if srcport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " source port " + srcport)
        
    if destaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " destination address " + destaddr)
        
    if destport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " destination port " + destport)
        
    if protocol:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " protocol " + str(protocol).lower())
        
    if transaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address " + transaddr)  
    else:
        if masquerade:  
            commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address masquerade")
        
    if transport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation port " + transport)  
            
    if disable:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " disable")  
            
    if exclude:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " exclude")  
        
    return FabricUtilNFV.send_vyatta_command(commands)
    
def create_nat(vmid, params):
    logger.debug("create_nat call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(create_nat_task, hosts=[addr], natinfo = params)

    return results[addr]
    
def get_nat(vmid, rulenum, ruletype):
    logger.debug("get_nat call!!")
    
    vm = get_vm(vmid)
    
    results = []
    nats = FabricUtilNFV.getNATs(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for nat in nats:
        if ruletype:
            if ruletype == "source" and nat['isSource'] ==  True:
                if rulenum:
                    if rulenum == nat['rule']:
                        results.append(nat)
                else:
                    results.append(nat)
            elif ruletype == "destination" and nat['isSource'] == False:
                if rulenum:
                    if rulenum == nat['rule']:
                        results.append(nat)
                else:
                    results.append(nat)
        else:
            if rulenum:
                if rulenum == nat['rule']:
                    results.append(nat)
            else:
                results.append(nat)
             
    return results    
    
def update_nat_task(natinfo):
    rulenum = natinfo['rulenum']
    ruletype = natinfo['ruletype']
    
    if 'ibnic' in natinfo:
        ibnic = natinfo['ibnic']
    else:
        ibnic = None
    
    if 'obnic' in natinfo:
        obnic = natinfo['obnic']
    else:
        obnic = None
    
    if 'srcaddr' in natinfo:
        srcaddr = natinfo['srcaddr']
    else:
        srcaddr = None
    
    if 'destaddr' in natinfo:
        destaddr = natinfo['destaddr']
    else:
        destaddr = None
    
    if 'srcport' in natinfo:
        srcport = natinfo['srcport']
    else:
        srcport = None
    
    if 'destport' in natinfo:
        destport = natinfo['destport']
    else:
        destport = None
    
    if 'protocol' in natinfo:
        protocol = natinfo['protocol']
    else:
        protocol = None
    
    if 'transaddr' in natinfo:
        transaddr = natinfo['transaddr']
    else:
        transaddr = None
    
    if 'transport' in natinfo:
        transport = natinfo['transport']
    else:
        transport = None
    
    if 'masquerade' in natinfo:
        masquerade = natinfo['masquerade']
    else:
        masquerade = None
    
    if 'disable' in natinfo:
        disable = natinfo['disable']
    else:
        disable = None
    
    if 'exclude' in natinfo:
        exclude = natinfo['exclude']
    else:
        exclude = None
        
    commands = []
    
    if ruletype == "destination" and ibnic:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " inbound-interface " + ibnic)
        
    if ruletype == "source" and obnic:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " outbound-interface " + obnic)
    
    if srcaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " source address " + srcaddr)
    
    if srcport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " source port " + srcport)
        
    if destaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " destination address " + destaddr)
        
    if destport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " destination port " + destport)
        
    if protocol:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " protocol " + str(protocol).lower())
        
    if transaddr:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address " + transaddr)  
    else:
        if masquerade:  
            commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address masquerade")
        
    if transport:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation port " + transport)  
            
    if disable:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " disable")  
            
    if exclude:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " exclude")  
        
            
    return FabricUtilNFV.send_vyatta_command(commands)

def update_nat(vmid, params):
    logger.debug("update_nat call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(update_nat_task, hosts=[addr], natinfo = params)

    return results[addr]
    
def delete_nat_task(natinfo):
    rulenum = natinfo['rulenum']
    ruletype = natinfo['ruletype']
    
    commands = []
    commands.append("$DELETE nat " + ruletype + " rule " + rulenum)
        
    return FabricUtilNFV.send_vyatta_command(commands)
    
def delete_nat(vmid, params):
    logger.debug("delete_nat call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(delete_nat_task, hosts=[addr], natinfo = params)

    return results[addr]