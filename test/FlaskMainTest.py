#-*- coding: utf-8 -*-
'''
Created on 2014. 9. 5.

@author: jerryj
'''

import requests
import json
import sys
import unittest

class FlaskMainTestCase(unittest.TestCase):
	name = 'kvmhost_jerryj'
	
	def testCreateVMHost_and_Register(self):
		headers = {'content-type': 'application/json'}
		
		results = requests.get('http://localhost:5001/vmhostbyname/' + self.name, headers=headers)
		print "GET /vmhostbyname %d" % results.status_code
		if results.status_code == 200:
			id = results.json()['_id']
		
			print json.dumps(results.json(), indent=4)
			
			results = requests.delete('http://localhost:5001/vmhost/' + id, headers = headers)
			
			print "DELETE /vmhost"
			print json.dumps(results.json(), indent=4)
		
		jsonData = {
		    "name": self.name,
		    'location': '대전',
		    "addr": "192.168.0.244",
		    "sshid": "root",
		    "sshpw": "redhat"
		}
		
		results = requests.post('http://localhost:5001/vmhost', data=json.dumps(jsonData), headers=headers)
		token = results.json()['token']
		
		print "POST /vmhost"
		print json.dumps(results.json(), indent=4)

	def testRegisterVM(self):
		headers = {'content-type': 'application/json'}
		
		results = requests.get('http://localhost:5001/vmhostbyname/' + self.name, headers=headers)
		print "GET /vmhostbyname %d" % results.status_code
		vmHostId = results.json()['_id']
			
		jsonData = {
		    "vmhost": vmHostId,
		    "type":"nfv",
		    "name": "kvm001",
		    "hostname": "vyatta",
		    "addr": "vyatta",
		    "sshid": "vyatta",
		    "sshpw": "vyatta",
		    "vmtype": "kvm",
		    "vendor": "vyatta",
		    "interfaces": [
		        {
		            "nic": "eth2",
		            "addr": "192.168.56.13"
		        }
			]
		}
	
		results = requests.post('http://localhost:5001/vm', data=json.dumps(jsonData), headers=headers)
		id = results.json()['_id']
		
		print "POST /vm"
		print json.dumps(results.json(), indent=4)
		
		requests.delete('http://localhost:5001/vm/' + id)
		
	def testGetAllVMHost(self):
		results = requests.get('http://localhost:5001/mon/vmhost/_all')
		if results.status_code == 200:
			print "GET /mon/vmhost/_all"
			print json.dumps(results.json(), indent=4)
		else:
			print results.status_code, results.content
	
	def testGetAllVM(self):
		results = requests.get('http://localhost:5001/mon/vm/_all')
		if results.status_code == 200:
			print "GET /mon/vm/_all"
			print json.dumps(results.json(), indent=4)
		else:
			print results.status_code, results.content
	
	def testGetVMByHost(self):
		headers = {'content-type': 'application/json'}
		
		results = requests.get('http://localhost:5001/vmhostbyname/' + self.name, headers=headers)
		print "GET /vmhostbyname %d" % results.status_code
		vmHostId = results.json()['_id']

		results = requests.get('http://localhost:5001/mon/vmbyhost/' + vmHostId)
		if results.status_code == 200:
			print "GET /mon/vmbyhost"
			print json.dumps(results.json(), indent=4)
		else:
			print results.status_code, results.content
	
# 	def testGraphite(self):
# 		results = requests.get('http://localhost:5001/mon/graphite?width=786&height=508&_salt=1410357564.227&target=vyatta.cpu.0.cpu.user.value&from=-3minutes')
# 		if results.status_code == 200:
# 			print json.dumps(results.json(), indent=4)
# 		else:
# 			print results.status_code, results.content

if __name__ == "__main__":
	unittest.main()


