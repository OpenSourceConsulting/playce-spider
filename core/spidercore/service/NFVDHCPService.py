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
Created on 2014. 11. 12.

Vyatta DHCP 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
from spidercore import FabricUtilNFV

logger = logging.getLogger(__name__)

def get_dhcp(vmid): 
    logger.debug("get_dhcp call!!")
    
    vm = get_vm(vmid)
    
    result = {}
    services = FabricUtilNFV.getServices(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for service in services:
        if 'service' in service and service['service'] == 'dhcp-server':
            result = service

    return result

def set_dhcp_global_task(dhcpinfo):
    if 'disabled' in dhcpinfo:
        disabled = dhcpinfo['disabled']
    else:
        disabled = None
    
    if 'dynamic_dns_update' in dhcpinfo:
        dynamic_dns_update = dhcpinfo['dynamic_dns_update']
    else:
        dynamic_dns_update = None
    
    if 'parameters' in dhcpinfo:
        parameters = dhcpinfo['parameters']
    else:
        parameters = None        
        
    commands = []
    
    if disabled and (disabled == True or disabled == 'true'):
        commands.append("$SET service dhcp-server disabled true")
    else:
        commands.append("$SET service dhcp-server disabled false")
        
    if dynamic_dns_update and (dynamic_dns_update == True or dynamic_dns_update == 'true'):
        commands.append("$SET service dhcp-server dynamic-dns-update enable true")
    else:
        commands.append("$SET service dhcp-server dynamic-dns-update enable false")
        
    commands.append("$DELETE service dhcp-server global-parameters")
    
    if parameters:
        params = parameters.split(',')
        
        for param in params:
            commands.append("$SET service dhcp-server global-parameters '" + param + "'")
            
    return FabricUtilNFV.send_vyatta_command(commands)

def set_dhcp_global(vmid, params):
    logger.debug("set_dhcp_global call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(set_dhcp_global_task, hosts=[addr], dhcpinfo = params)

    return results[addr]

def set_dhcp_task(dhcpinfo):
    if 'disable' in dhcpinfo:
        disable = dhcpinfo['disable']
    else:
        disable = None
    
    if 'authoritative' in dhcpinfo:
        authoritative = dhcpinfo['authoritative']
    else:
        authoritative = None
        
    if 'shared_network_name' in dhcpinfo:
        shared_network_name = dhcpinfo['shared_network_name']
    else:
        shared_network_name = None
    
    if 'subnet_ipv4net' in dhcpinfo:
        subnet_ipv4net = dhcpinfo['subnet_ipv4net']
    else:
        subnet_ipv4net = None   
         
    if 'start_ip' in dhcpinfo:
        start_ip = dhcpinfo['start_ip']
    else:
        start_ip = None 
         
    if 'stop_ip' in dhcpinfo:
        stop_ip = dhcpinfo['stop_ip']
    else:
        stop_ip = None 
         
    if 'default_router' in dhcpinfo:
        default_router = dhcpinfo['default_router']
    else:
        default_router = None 
         
    if 'dns_server' in dhcpinfo:
        dns_server = dhcpinfo['dns_server']
    else:
        dns_server = None
         
    if 'domain_name' in dhcpinfo:
        domain_name = dhcpinfo['domain_name']
    else:
        domain_name = None
         
    if 'static_mapping' in dhcpinfo:
        static_mapping = dhcpinfo['static_mapping']
    else:
        static_mapping = None
    
    commands = []
    
    if shared_network_name:
        if subnet_ipv4net and start_ip and stop_ip:
            # 1. Set shared-network-name (require : name, ipv4net, start, stop)
            commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " start " + start_ip + " stop " + stop_ip)
        
            # 2. Set or Delete default-router
            if default_router:
                commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " default-router " + default_router)
            else:
                commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " default-router")
            
            # 3. Delete and Set dns-server
            commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " dns-server")
            if dns_server:
                dnsservers = dns_server.split(',')
                
                for dnsserver in dnsservers:
                    commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " dns-server " + dnsserver)
            
            # 4. Set of Delete domain-name
            if domain_name:
                commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " domain-name " + domain_name)
            else:
                commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " domain-name")
                            
            # 5. Delete and Set static-mapping
            commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " static-mapping")
            
            if static_mapping:
                for mapping in static_mapping:
                    commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " static-mapping " + mapping['map_name'] + " ip-address " + mapping['map_ip'])
                    commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " subnet " + subnet_ipv4net + " static-mapping " + mapping['map_name'] + " mac-address " + mapping['map_mac'])
            
        # 6. Set or Delete authoritative
        if authoritative and (authoritative == True or authoritative == 'true'):
            commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " authoritative enable")
        else:
            commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " authoritative disable")
        
        # 7. Set of Delete disable
        if disable and (disable == True or disable == 'true'):
            commands.append("$SET service dhcp-server shared-network-name " + shared_network_name + " disable")
        else:
            commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name + " disable")
         
    return FabricUtilNFV.send_vyatta_command(commands)

def set_dhcp(vmid, params):
    logger.debug("set_dhcp call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(set_dhcp_task, hosts=[addr], dhcpinfo = params)

    return results[addr]

def delete_dhcp_task(dhcpinfo): 
    if 'shared_network_name' in dhcpinfo:
        shared_network_name = dhcpinfo['shared_network_name']
    else:
        shared_network_name = None
        
    if 'is_last' in dhcpinfo:
        is_last = dhcpinfo['is_last']
    else:
        is_last = None
        
    commands = []
    
    if is_last and (is_last == True or is_last == 'true'):
        commands.append("$DELETE service dhcp-server")
    else:
        if shared_network_name:
            commands.append("$DELETE service dhcp-server shared-network-name " + shared_network_name)
            
    return FabricUtilNFV.send_vyatta_command(commands)

def delete_dhcp(vmid, params):
    logger.debug("delete_dhcp call!!")
    
    vm = get_vm(vmid)
    addr = vm['mgraddr']
    
    env.hosts = [ addr ]
    env.user = vm['sshid']
    env.password = vm['sshpw']
    env.shell = '/bin/vbash -ic'
    results = execute(delete_dhcp_task, hosts=[addr], dhcpinfo = params)

    return results[addr]