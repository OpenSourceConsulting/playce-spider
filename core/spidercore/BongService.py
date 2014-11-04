#-*- coding: utf-8 -*-
'''---------------------------
    Sample Service
    
    Created on 2014. 11. 3.
    @author: Bong-Jin Kwon
---------------------------'''
from spidercore import *
#import logging


logger = logging.getLogger(__name__)

def service_method(name):
    logger.debug("service log message.")
    return "Hello " + name + "!"

def foo():
    logger.info('Hi, foo')

class Bar(object):
    def bar(self):
        logger.info('Hi, bar')