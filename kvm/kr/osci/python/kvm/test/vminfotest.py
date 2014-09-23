'''
Created on Sep 18, 2014

@author: root
'''


import kr.osci.python.kvm.vminfo as vminfo
import kr.osci.python.kvm.vmcontroller as vmcontroller
from kr.osci.python.kvm import vmmodel


def print_section(title):
    print "\n%s" % title
    print "=" * 60

def print_entry(key, value):
    print "%-10s %-10s" % (key, value)

def print_xml(key, ctx, path):
    res = ctx.xpathEval(path)
    if res is None or len(res) == 0:
        value="Unknown"
    else:
        value = res[0].content
    print_entry(key, value)
    return value



print_section("Virtual Machine All List")
print vminfo.list_vms()
"""
print 

print_section("Running vmList")
print vminfo.list_active_vms()
print 

print_section("Shutdown vmList")
print vminfo.list_inactive_vms()
print 

print_section("detail VM Info")
print_entry(vminfo.list_inactive_vms()[0],vminfo.vm_info(vminfo.list_inactive_vms()[0]))
print_entry("nics",vminfo.get_nics(vminfo.list_inactive_vms()[0]))
print_entry("macs",vminfo.get_macs(vminfo.list_inactive_vms()[0]))
print_entry("xml",vminfo.get_xml(vminfo.list_inactive_vms()[0]))
print_entry("xml",vminfo.get_xml(vminfo.list_inactive_vms()[0]))
print 




print_section("detail VM Info")
print vminfo.list_inactive_vms()[0]
print vminfo._get_dom("test04")
print vminfo.vm_state("test04")
print vminfo.vm_info("test04")


print_section("running index[0] name")
print vminfo._get_vm(vminfo.list_active_vms()[0])
print_entry("state",vminfo.vm_state(vminfo.list_active_vms()[0]))

print_section("shutdown index[0] name")
print vminfo._get_vm(vminfo.list_inactive_vms()[0])
print_entry("state",vminfo.vm_state(vminfo.list_inactive_vms()[0]))
"""


print_section("shutdown index[0] status")
print_entry("name",vminfo.list_inactive_vms()[0])
print_entry("status",vmcontroller.state(vminfo.list_inactive_vms()[0]))


#print_entry("start",vmcontroller.start(vminfo.list_inactive_vms()[0]))


#print_entry("shutdown",vmcontroller.shutdown("test04"))



