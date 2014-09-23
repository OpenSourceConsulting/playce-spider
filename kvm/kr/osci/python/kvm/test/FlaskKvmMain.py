'''
Created on Sep 14, 2014

@author: mwchoi
'''
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

import libvirt
import json
import codecs
import uuid
import requests


from kr.osci.python.kvm.vmmodel import VM

import kr.osci.python.kvm.vminfo as vminfo
import kr.osci.python.kvm.vmcontroller as vmcontroller




#    KVM Controller API
@app.route("/kvm/list_vms", methods=['GET'])
def vminfo_list_vms():
    list = vminfo.list_vms()
    return json.dumps(list)

@app.route("/kvm/list_active_vms", methods=['GET'])
def vminfo_list_active_vms():
    list = vminfo.list_active_vms() 
    return json.dumps(list)


@app.route("/kvm/list_inactive_vms", methods=['GET'])
def vminfo_list_inactive_vms():
    list =  vminfo.list_inactive_vms()
    return json.dumps(list)


@app.route("/kvm/createDomain/<name>", methods=['GET'])
def kvm_createVm(name=None):
    if name == None:
        name = "test_01"
#        return "No unique name for VM Host", 404
    
    objectVm = VM()
    objectVm.set_name(name)
    objectVm.set_ram(1024)
    objectVm.set_vcpus(2)
    objectVm.set_kvm_nested(True)
    objectVm.set_template("template_02")

    print objectVm


#    return vmcontroller.clonevm(objectVm).clone() 
    return json.dumps(vmcontroller.clonevm(objectVm)) 


@app.route("/kvm/start/<name>", methods=['GET'])
def vmcontroller_start_vms(name=None):
    if name == None:
        name = "CactiEz"
    
    return json.dumps(vmcontroller.start(name))


@app.route("/kvm/shutdown/<name>", methods=['GET'])
def vmcontroller_shutdown_vms(name=None):
    if name == None:
        name = "CactiEz"
    
    return json.dumps(vmcontroller.shutdown(name))



@app.route("/kvm/status/<name>", methods=['GET'])
def vmcontroller_state_vms(name=None):
    if name == None:
        name = "CactiEz"
    
    return json.dumps(vmcontroller.state(name))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

