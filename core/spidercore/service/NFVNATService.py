#-*- coding: utf-8 -*-
'''
Created on 2014. 11. 7.

Vyatta NAT 제어 모듈

@author: Sang-Cheon Park
'''

from spidercore import *
from fabric.api import env
from fabric.tasks import execute
import spidercore.FabricUtilNFV

logger = logging.getLogger(__name__)

def create_nat_task(natinfo):
    ruleid = natinfo['ruleid']
    ruletype = natinfo['ruletype']
    
    commands = []
    commands.append("$SET nat " + ruletype + " rule " + ruleid)
    
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
    
def all_nats(vmid):
    vm = get_vm(vmid)
    return FabricUtilNFV.getNATs(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    
def update_nat_task(natinfo):
    ruleid = natinfo['ruleid']
    ruletype = natinfo['ruletype']
    ibnic = natinfo['ibnic']
    obnic = natinfo['obnic']
    srcaddr = natinfo['srcaddr']
    destaddr = natinfo['destaddr']
    srcport = natinfo['srcport']
    destport = natinfo['destport']
    protocol = natinfo['protocol']
    translation = natinfo['translation']
    masquerade = natinfo['masquerade']
    
    commands = []
    
    if ibnic:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " inbound-interface " + ibnic)
        
    if obnic:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " outbound-interface " + obnic)
    
    if srcaddr:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " source address " + srcaddr)
    
    if srcport:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " source port " + srcport)
        
    if destaddr:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " destination address " + destaddr)
        
    if destport:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " destination port " + destport)
        
    if protocol:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " protocol " + str(protocol).lower())
        
    if masquerade:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " translation address masquerade")
    elif translation:
        commands.append("$set nat " + ruletype + " rule " + ruleid + " translation address " + translation)    
        
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
    ruleid = natinfo['ruleid']
    commands = []
    
    commands.append("$DELETE nat rule " + ruleid)
        
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