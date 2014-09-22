'''
Created on Sep 12, 2014

@author: mwchoi

Work with virtual machines managed by libvirt
:depends: libvirt Python module

'''
#nfv import
import vminfo
import subprocess


def state(vm_):
    dom = vminfo._get_dom(vm_)
    
#    return dom.state(False)
    return vminfo.vm_state(vm_)
    
   
def shutdown(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.shutdown() == 0
   
   
def pause(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.suspend() == 0
   
   
def resume(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.resume() == 0
   

def create(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.create() == 0
   
   
def start(vm_):
    return create(vm_)
   
   
def reboot(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.reboot(0) == 0
   
   
def reset(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.reset(0) == 0
   
   
def destroy(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.destroy() == 0
   
   
def undefine(vm_):
    dom = vminfo._get_dom(vm_)
    return dom.undefine() == 0



def clonevm(self):
    cmd = []
    cmd.append("virt-clone")
    cmd.append("-o")
    cmd.append(self.get_template())
    cmd.append("-n")
    cmd.append(self.get_name())
    cmd.append("-f")
    cmd.append("/data/libvirt/images/" + self.get_name() + ".img")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    return p.communicate()