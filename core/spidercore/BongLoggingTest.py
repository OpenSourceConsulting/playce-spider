#-*- coding: utf-8 -*-
'''---------------------------------
    Simple Logging Demo 
    
    Created on 2014. 11. 3.
    @author: Bong-Jin Kwon
---------------------------------'''
import os
import json
import logging.config
import BongService

# load the logging configuration
#logging.config.fileConfig('../conf/logging.conf2', disable_existing_loggers=False)

# http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
def setup_logging(
    default_path='../conf/log_conf.json', 
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """ 
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        logging.info("logging: load "+ os.path.abspath(path))
    else:
        logging.basicConfig(level=default_level)
        logging.info("logging: set basic config.")
        
"""
# Logging Test

setup_logging()

BongService.foo()
bar = BongService.Bar()
bar.bar()
"""