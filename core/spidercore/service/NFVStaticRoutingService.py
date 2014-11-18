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
Created on 2014. 11. 14.

Vyatta Static Routing 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV

logger = logging.getLogger(__name__)

# Case 460 : Static Routing 기능 구현

def get_static_routing(vmid): 
    logger.debug("get_static_routing call!!")
    
    vm = get_vm(vmid)
    
    result = {}
    protocols = FabricUtilNFV.getProtocols(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for protocol in protocols:
        if 'protocol' in protocol and protocol['protocol'] == 'static':
            result = protocol

    return result

def flush_static_routing_task():
    commands = []
    commands.append("$RESET ip route cache")
            
    return FabricUtilNFV.send_vyatta_command(commands)
    
def flush_static_routing(vmid):
    logger.debug("flush_static_routing call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(flush_static_routing_task, hosts=[addr])

    return results[addr]

def set_static_routing_task(routinginfo):
    if 'routing_subnet' in routinginfo:
        routing_subnet = routinginfo['routing_subnet']
    else:
        routing_subnet = None
        
    if 'routing_type' in routinginfo:
        routing_type = routinginfo['routing_type']
    else:
        routing_type = None
        
    if 'routing_table' in routinginfo:
        routing_table = routinginfo['routing_table']
    else:
        routing_table = None
        
    if 'routing_next_hop' in routinginfo:
        routing_next_hop = routinginfo['routing_next_hop']
    else:
        routing_next_hop = None
        
    if 'routing_distance' in routinginfo:
        routing_distance = routinginfo['routing_distance']
    else:
        routing_distance = 1
        
    if 'routing_blackhole' in routinginfo:
        routing_blackhole = routinginfo['routing_blackhole']
    else:
        routing_blackhole = None
        
    if 'routing_disable' in routinginfo:
        routing_disable = routinginfo['routing_disable']
    else:
        routing_disable = None
        
    if routing_distance == None or int(routing_distance) <= 0 or int(routing_distance) > 255:
        routing_distance = 1
        
    commands = []
    
    if routing_table and int(routing_table) > 0 and int(routing_table) < 256:
        if routing_type == "route":
            if routing_blackhole and (routing_blackhole == True or routing_blackhole == "true"):
                commands.append("$SET protocols static table " + str(routing_table) + " route " + routing_subnet + " blackhole" + " distance " + str(routing_distance))
            else:
                commands.append("$SET protocols static table " + str(routing_table) + " route " + routing_subnet + " next-hop " + routing_next_hop + " distance " + str(routing_distance))
                
                if routing_disable and (routing_disable == True or routing_disable == "true"):
                    commands.append("$SET protocols static table " + str(routing_table) + " route " + routing_subnet + " next-hop " + routing_next_hop + " disable")
        else:
            if routing_blackhole and (routing_blackhole == True or routing_blackhole == "true"):
                commands.append("$SET protocols static table " + str(routing_table) + " interface-route " + routing_subnet + " blackhole" + " distance " + str(routing_distance))
            else:
                commands.append("$SET protocols static table " + str(routing_table) + " interface-route " + routing_subnet + " next-hop-interface " + routing_next_hop + " distance " + str(routing_distance))
                
                if routing_disable and (routing_disable == True or routing_disable == "true"):
                    commands.append("$SET protocols static table " + str(routing_table) + " interface-route " + routing_subnet + " next-hop-interface " + routing_next_hop + " disable")
    else:
        if routing_type == "route":
            if routing_blackhole and (routing_blackhole == True or routing_blackhole == "true"):
                commands.append("$SET protocols static route " + routing_subnet + " blackhole" + " distance " + str(routing_distance))
            else:
                commands.append("$SET protocols static route " + routing_subnet + " next-hop " + routing_next_hop + " distance " + str(routing_distance))
                
                if routing_disable and (routing_disable == True or routing_disable == "true"):
                    commands.append("$SET protocols static route " + routing_subnet + " next-hop " + routing_next_hop + " disable")
        else:
            if routing_blackhole and (routing_blackhole == True or routing_blackhole == "true"):
                commands.append("$SET protocols static interface-route " + routing_subnet + " blackhole" + " distance " + str(routing_distance))
            else:
                commands.append("$SET protocols static interface-route " + routing_subnet + " next-hop-interface " + routing_next_hop + " distance " + str(routing_distance))
                
                if routing_disable and (routing_disable == True or routing_disable == "true"):
                    commands.append("$SET protocols static interface-route " + routing_subnet + " next-hop-interface " + routing_next_hop + " disable")
        
    return FabricUtilNFV.send_vyatta_command(commands)

def set_static_routing(vmid, params):
    logger.debug("set_static_routing call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(set_static_routing_task, hosts=[addr], routinginfo = params)

    return results[addr]

def delete_static_routing_task(routinginfo):
    if 'routing_subnet' in routinginfo:
        routing_subnet = routinginfo['routing_subnet']
    else:
        routing_subnet = None
        
    if 'routing_type' in routinginfo:
        routing_type = routinginfo['routing_type']
    else:
        routing_type = None
        
    if 'routing_table' in routinginfo:
        routing_table = routinginfo['routing_table']
    else:
        routing_table = None
        
    if 'is_last_in_table' in routinginfo:
        is_last_in_table = routinginfo['is_last_in_table']
    else:
        is_last_in_table = None
        
    commands = []
    
    if routing_table and routing_table != "":
        if is_last_in_table and (is_last_in_table == True or is_last_in_table == "true"):
            commands.append("$DELETE protocols static table " + routing_table)
        else:
            if routing_type == "route":
                commands.append("$DELETE protocols static table " + routing_table + " route " + routing_subnet)
            else:
                commands.append("$DELETE protocols static table " + routing_table + " interface-route " + routing_subnet)
    else:
        if routing_type == "route":
            commands.append("$DELETE protocols static route " + routing_subnet)
        else:
            commands.append("$DELETE protocols static interface-route " + routing_subnet)
        
    return FabricUtilNFV.send_vyatta_command(commands)

def delete_static_routing(vmid, params):
    logger.debug("delete_static_routing call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(delete_static_routing_task, hosts=[addr], routinginfo = params)

    return results[addr]