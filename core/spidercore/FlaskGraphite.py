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
Created on 2014. 9. 29.

@author: jerryj
'''

from spidercore import *
from flask import Flask, request, Response
import json
import requests

#	Monitoring API

@app.route("/mon/graphite", methods=['GET'])
def mon_graphite():
	queryStr = request.query_string
	result = requests.get('http://localhost:8000/render?' + queryStr + '&format=json').json()
	for metric in result:
		datapoints = metric['datapoints']
		newDatapoints = []
		for val in datapoints:
			newVal = { "value": val[0], "date": val[1]}
			newDatapoints.append(newVal)
		metric['datapoints'] = newDatapoints
	return json.dumps(result) + '\n'

@app.route("/mon/graphite/center/<centerId>", methods=['GET'])
def mon_graphite_center_status(centerId=None):
	if centerId == None:
		return "No id for center", 404

	locations = read_repository('locations')
	vmhosts = read_repository('vmhosts')
	targetVmhosts = []
	for center in locations:
		if center['name'] == centerId:
			for vmhost in vmhosts:
				if vmhost['location'] == centerId:
					targetVmhosts.append(vmhost)
	else:
		return "Invalid center ID", 404

	#	Collecting CPU usage for vmhosts belonging to the location/center	
	timespan = "1"
	timeunit = "minutes"
	for vmhost in targetVmhosts:
		vmhostId = vmhost['hostname']
		url = "http://localhost:8000/render/?width=500&height=500&from=-%s%s&format=json" % (timespan, timeunit)
		url += "&target=averageSeries(%s.cpu.*.cpu.system.value)&target=averageSeries(%s.cpu.*.cpu.user.value)" % (vmhostId, vmhostId)
		result = requests.get(url).json()
		return json.dumps(result) + '\n'

	return "AAAAAAAAAAAAAa"


#	http://192.168.0.130:8000/render/?width=786&height=508&_salt=1417023959.735
#	target=111cc0cf-585c-42d8-8306-327f004aaa03.cpu.*.cpu.{user,system}.value&from=-30seconds
@app.route("/mon/graphite/vmhostcpu/<vmhostId>", methods=['GET'])
def mon_graphite_vmhostcpu(vmhostId=None):
	if vmhostId == None:
		return "No id for VM", 404

	idtoname = {}
	vms = read_repository('vms')
	indexes = []
	for vm in vms:
		if vm['vmhost'] == vmhostId:
			indexes.append("target=%s.cpu.*.cpu.{user,system}.value" % vm['_id'])
			idtoname[vm['_id']] = vm['vmname']
	url = ""
	for idx in indexes:
		url += idx + '&' 
	url += 'from=-30seconds&format=json'
	url = 'http://localhost:8000/render/?' + url
	logging.info("URL %s" % url)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints

	cpuResult = {}
	size = 0
	for metric in result:
		target = metric['target'].split('.')
		vmid, cpuid, valtype = target[0], target[2], target[4]
		if vmid not in cpuResult:
			cpuResult[vmid] = {}
		if cpuid not in cpuResult[vmid]:
			cpuResult[vmid][cpuid] = {}
		cpuResult[vmid][cpuid][valtype] = []
		
		size = len(metric['datapoints'])
		for val in metric['datapoints']:
			cpuResult[vmid][cpuid][valtype].append(val['value'])
		
	for vmid in cpuResult:
		cpuSum = 0.0
		for cpuid in cpuResult[vmid]:
			sum = 0.0
			noneCount = 0
			for i in range(0, size):
				for valtype in cpuResult[vmid][cpuid]:
					if cpuResult[vmid][cpuid][valtype][i] == None:
						noneCount += 1
					else:
						sum += cpuResult[vmid][cpuid][valtype][i]
			avg = sum / (size - noneCount)
			cpuSum += avg
		cpuResult[vmid]['cpuavg'] = cpuSum / len(cpuResult[vmid])  

	result = {}
	for vmid in cpuResult:
		result[vmid] = {'value': cpuResult[vmid]['cpuavg']}
		result[vmid]['vmname'] = idtoname[vmid]
		
	return json.dumps(result) + '\n'

#	111cc0cf-585c-42d8-8306-327f004aaa03.memory.memory.used.value
@app.route("/mon/graphite/vmhostmem/<vmhostId>", methods=['GET'])
def mon_graphite_vmhostmem(vmhostId=None):
	if vmhostId == None:
		return "No id for VM", 404

	idtoname = {}
	vms = read_repository('vms')
	indexes = []
	for vm in vms:
		if vm['vmhost'] == vmhostId:
			indexes.append("target=%s.memory.memory.used.value" % vm['_id'])
			idtoname[vm['_id']] = vm['vmname']
	url = ""
	for idx in indexes:
		url += idx + '&' 
	url += 'from=-30seconds&format=json'
	url = 'http://localhost:8000/render/?' + url
	logging.info("URL %s" % url)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints

	memResult = {}
	size = 0
	for metric in result:
		target = metric['target'].split('.')
		vmid, memid, valtype = target[0], target[2], target[3]
		if vmid not in memResult:
			memResult[vmid] = {}
		if memid not in memResult[vmid]:
			memResult[vmid][memid] = {}
		memResult[vmid][memid][valtype] = []
		
		size = len(metric['datapoints'])
		for val in metric['datapoints']:
			memResult[vmid][memid][valtype].append(val['value'])
		
	for vmid in memResult:
		memSum = 0.0
		for memid in memResult[vmid]:
			sum = 0.0
			noneCount = 0
			for i in range(0, size):
				for valtype in memResult[vmid][memid]:
					if memResult[vmid][memid][valtype][i] == None:
						noneCount += 1
					else:
						sum += memResult[vmid][memid][valtype][i]
			avg = sum / (size - noneCount)
			memSum += avg
		memResult[vmid]['memavg'] = memSum / len(memResult[vmid])  

	result = {}
	for vmid in memResult:
		result[vmid] = {'value': memResult[vmid]['memavg']}
		result[vmid]['vmname'] = idtoname[vmid]
		
	return json.dumps(result) + '\n'

# 111cc0cf-585c-42d8-8306-327f004aaa03.interface.if_packets.eth0.tx
@app.route("/mon/graphite/vmhostnet/<vmhostId>", methods=['GET'])
def mon_graphite_vmhostnet(vmhostId=None):
	if vmhostId == None:
		return "No id for VM", 404

	idtoname = {}
	vms = read_repository('vms')
	indexes = []
	for vm in vms:
		if vm['vmhost'] == vmhostId:
			indexes.append("target=%s.interface.if_packets.*.{tx,rx}" % vm['_id'])
			idtoname[vm['_id']] = vm['vmname']
	url = ""
	for idx in indexes:
		url += idx + '&' 
	url += 'from=-30seconds&format=json'
	url = 'http://localhost:8000/render/?' + url
	logging.info("URL %s" % url)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints

	netResult = {}
	size = 0
	for metric in result:
		target = metric['target'].split('.')
		vmid, nicid, valtype = target[0], target[3], target[4]
		if vmid not in netResult:
			netResult[vmid] = {}
		if nicid not in netResult[vmid]:
			netResult[vmid][nicid] = {}
		netResult[vmid][nicid][valtype] = []
		
		size = len(metric['datapoints'])
		for val in metric['datapoints']:
			netResult[vmid][nicid][valtype].append(val['value'])
		
	for vmid in netResult:
		netSum = 0.0
		for nicid in netResult[vmid]:
			sum = 0.0
			noneCount = 0
			for i in range(0, size):
				for valtype in netResult[vmid][nicid]:
					if netResult[vmid][nicid][valtype][i] == None:
						noneCount += 1
					else:
						sum += netResult[vmid][nicid][valtype][i]
			avg = sum / (size - noneCount)
			netSum += avg
		netResult[vmid]['netavg'] = netSum / len(netResult[vmid])  

	result = {}
	for vmid in netResult:
		result[vmid] = {'value': netResult[vmid]['netavg']}
		result[vmid]['vmname'] = idtoname[vmid]
		
	return json.dumps(result) + '\n'


@app.route("/mon/graphite/cpu/<vmid>", methods=['GET'])
def mon_graphite_cpu(vmid=None):
	if vmid == None:
		return "No id for VM", 404

	# hours, days, minutes, seconds
	timespan = request.args.get('timespan')
	timeunit = request.args.get('timeunit')
	url = "http://localhost:8000/render/?width=500&height=500&from=-%s%s&format=json" % (timespan, timeunit)
	url += "&target=averageSeries(%s.cpu.*.cpu.system.value)&target=averageSeries(%s.cpu.*.cpu.user.value)" % (vmid, vmid)
	result = requests.get(url).json()
	
	numofcore = 1.0
	if vmid == 'Lion':
		numofcore = 4
	elif vmid == 'nipa_host':
		numofcore = 8
	elif vmid == 'kvmhost2':
		numofcore = 2
	print "NumOfCore: %d %s" % (numofcore, vmid)
	for metric in result:
		for data in metric['datapoints']:
			if data['value'] != None:
				data['value'] = data['value'] / numofcore
			
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints
	return json.dumps(result) + '\n'


@app.route("/mon/graphite/interface/<vmid>", methods=['GET'])
def mon_graphite_interface(vmid=None):
	if vmid == None:
		return "No id for VM", 404

	# hours, days, minutes, seconds
	timespan = request.args.get('timespan')
	timeunit = request.args.get('timeunit')
	mode = request.args.get('mode')
	nic = request.args.get('nic')
	if mode == None or mode == '':
		mode = 'both'
	if nic == None or nic == '':
		nic = 'eth*'
	func1 = func2 = ''
	if timeunit == 'days':
		func1 = 'summarize('
		func2 = ", '%s00minute', 'avg')" % (timespan,)
	elif timeunit == 'hours':
		func1 = 'summarize('
		func2 = ", '%s00second', 'avg')" % (timespan,)
	elif timeunit == 'minutes':
		func1 = 'summarize('
		func2 = ", '%ssecond', 'avg')" % (timespan,)
	url = "http://localhost:8000/render/?width=500&height=500&from=-%s%s&format=json" % (timespan, timeunit)
	if mode == 'txonly' or mode == 'both':
		url += "&target=%s%s.interface.if_octets.%s.tx%s" % (func1, vmid, nic, func2)
	if mode == 'rxonly' or mode == 'both':
		url += "&target=%s%s.interface.if_octets.%s.rx%s" % (func1, vmid, nic, func2)
	logging.debug("URL: " + url)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints
	return json.dumps(result) + '\n'


@app.route("/mon/graphite/memory/<vmid>", methods=['GET'])
def mon_graphite_memory(vmid=None):
	if vmid == None:
		return "No id for VM", 404

	# hours, days, minutes, seconds
	timespan = request.args.get('timespan')
	timeunit = request.args.get('timeunit')
	url = "http://localhost:8000/render/?width=500&height=500&from=-%s%s&format=json" % (timespan, timeunit)
	url += "&target=averageSeries(%s.memory.memory.used.value)" % (vmid)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints
	return json.dumps(result) + '\n'


@app.route("/mon/graphite/totalview", methods=['POST'])
def mon_graphite_totalview():
	# hours, days, minutes, seconds
	timespan = request.args.get('timespan')
	timeunit = request.args.get('timeunit')
	
#	cpuUrl = "http://oscjenkins.ddns.net:8000/render/?width=700&height=500&from=-%s%s" % (timespan, timeunit)
	cpuUrl = "http://oscjenkins.ddns.net:8000/render/?width=700&height=500&from=-%s%s&yMax=100" % (timespan, timeunit)
	nicUrl = "http://oscjenkins.ddns.net:8000/render/?width=700&height=500&from=-%s%s" % (timespan, timeunit)
	memUrl = "http://oscjenkins.ddns.net:8000/render/?width=700&height=500&from=-%s%s" % (timespan, timeunit)

	jsonData = request.json
	for vmid in jsonData:
		cpuUrl += "&target=sum(averageSeries(%s.cpu.*.cpu.system.value)&target=averageSeries(%s.cpu.*.cpu.user.value)" % (vmid, vmid)
		nicUrl += "&target=sum(%s.interface.if_octets.*.*)" % (vmid)
		memUrl += "&target=%s.memory.memory.used.value" % (vmid)

	result = {
		'cpu': cpuUrl,
		'nic': nicUrl,
		'mem': memUrl
	}

	return json.dumps(result, indent=4)


@app.route("/mon/ping", methods=['GET'])
def mon_ping():
	return json.dumps({ 'result': 'ok'})



