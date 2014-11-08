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
        
    if 'translation' in natinfo:
        translation = natinfo['translation']
    else:
        translation = None
    
    if 'masquerade' in natinfo:
        masquerade = natinfo['masquerade']
    else:
        masquerade = None
    
    commands = []
    
    if ruletype == "source":
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " outbound-interface " + obnic)
    else:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " inbound-interface " + ibnic)
        
    if translation:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address " + translation)  
    else:
        if masquerade:  
            commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address masquerade")
    
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
    
def get_nat(vmid, rulenum, ruletype):
    logger.debug("get_nat call!!")
    
    vm = get_vm(vmid)
    
    results = []
    nats = FabricUtilNFV.getNATs(vm['mgraddr'], vm['sshid'], vm['sshpw'])
    for nat in nats:
        if rulenum == nat['rule']:
            if ruletype:
                if ruletype == "source" and nat['isSource'] ==  True:
                    results.append(nat)
                elif ruletype == "destination" and nat['isSource'] == False:
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
    
    if 'translation' in natinfo:
        translation = natinfo['translation']
    else:
        translation = None
    
    if 'masquerade' in natinfo:
        masquerade = natinfo['masquerade']
    else:
        masquerade = None
        
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
        
    if translation:
        commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address " + translation)  
    else:
        if masquerade:  
            commands.append("$SET nat " + ruletype + " rule " + rulenum + " translation address masquerade")
            
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