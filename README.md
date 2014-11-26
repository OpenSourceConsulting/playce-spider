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

==Graphite== should be installed for monitoring data collection as follows (the guide is based on CentOS 7)

```
sudo yum install pycairo
sudo pip install 'django<1.6'
sudo pip install graphite-web
```

DB Creation

```
[jerryj@localhost graphite]$ pwd
/opt/graphite/webapp/graphite
[jerryj@localhost graphite]$ sudo python manage.py syncdb

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'root'): admin
Email address: non@none.com
Password: Your password
Password (again): Your password
```

Start Carbon

```
[jerryj@localhost graphite]$ sudo ./bin/carbon-cache.py  start
```

Start WebApp

```
[jerryj@localhost graphite]$ sudo pip install 'gunicorn==19.1'
[jerryj@localhost graphite]$ sudo gunicorn_django --workers=2 -b:8000
```

Start NTP server

```
[jerryj@localhost graphite]$ sudo yum install ntp 
[jerryj@localhost graphite]$ sudo vi /etc/ntp.conf
# Use public servers from the pool.ntp.org project.
# Please consider joining the pool (http://www.pool.ntp.org/join.html).
#server 0.centos.pool.ntp.org
#server 1.centos.pool.ntp.org
#server 2.centos.pool.ntp.org
server kr.pool.ntp.org
server time.bora.net
server time.kornet.net
[jerryj@localhost graphite]$ sudo service ntpd restart
```
