'''
Created on 2014. 9. 11.

@author: jerryj
'''

from fabric.api import run, sudo, put, env

def hello():
#	Hello Fabric!
	print "Hello, Fabric!"


def host_ls():
	run('ls -l')

def dev():
	env.hosts = [ 'jerryj@centos7', ]
	env.user = 'jerryj'
	env.password = 'ma1183'

def sudo_id():
	sudo('id')

def put_sh():
	sudo('id')
	put('fabfile.py', '~/')
	