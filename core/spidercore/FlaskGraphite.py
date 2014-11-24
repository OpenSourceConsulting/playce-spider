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


@app.route("/mon/graphite/vmhostcpu/<vmhostId>", methods=['GET'])
def mon_graphite_vmhostcpu(vmhostId=None):
	if vmhostId == None:
		return "No id for VM", 404

	vms = read_repository('vms')
	selected_vms = []
	for vm in vms:
		if vm['vmhost'] == vmhostId:
			selected_vms.append("sum(%s.cpu.*.cpu.system.value, %s.cpu.*.cpu.user.value)" % (vm['_id'], vm['_id']))
	fun = "averageSeries("
	first = True
	for f in selected_vms:
		if not first:
			fun += ','
		else:
			first = False
		fun += f
	fun += ")"
	# hours, days, minutes, seconds
	timespan = request.args.get('timespan')
	timeunit = request.args.get('timeunit')
	url = "http://localhost:8000/render/?width=500&height=500&from=-%s%s&format=json" % (timespan, timeunit)
	url += "&target=%s" % (fun)
	logging.info("URL %s" % url)
	result = requests.get(url).json()
# 	for metric in result:
# 		datapoints = metric['datapoints']
# 		newDatapoints = []
# 		for val in datapoints:
# 			newVal = { "value": val[0], "date": val[1]}
# 			newDatapoints.append(newVal)
# 		metric['datapoints'] = newDatapoints
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
	
	jsonData = request.json
	for vm in jsonData:
		vmid = vm['vmid'],
		metrics = vm['metrics']
		
	
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


@app.route("/mon/ping", methods=['GET'])
def mon_ping():
	return json.dumps({ 'result': 'ok'})
