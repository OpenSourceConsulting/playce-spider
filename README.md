Major features we're planning
- KVM Virtual Instance Managment
- NFV Device Management (NIC, loadbalancing, etc)
- NFV Device real-time Monitoring (system resources, health status, etc)
- Integrated management console UI for multiple virtual devices
- Automatic provisioning

* Github & FogBugz has been connected

Installation Guide

```
git clone https://github.com/OpenSourceConsulting/athena-spider
cd core
export PYTHON_PATH=.
python -m spidercore.FlaskMain
```

The following libraries are required.
```
Fabric==1.10.0
Flask==0.10.1
Flask-Cors==1.9.0
paramiko==1.15.1
pycrypto==2.6.1
pyparsing==2.0.3
requests==2.4.3
rpyc==3.3.0
```

Graphite should be installed for monitoring data collection

