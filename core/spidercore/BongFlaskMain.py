#-*- coding: utf-8 -*-
'''---------------------------------
    Simple Flask Demo 
     - 한글 주석 사용
     - logging 기능
     - service(비즈니스 로직) 분리
    
    Created on 2014. 11. 3.
    @author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *
#from flask import Flask
#import BongLoggingTest
import BongService



logger = logging.getLogger(__name__)

#app = Flask(__name__)


@app.route("/")
def hello():
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    return BongService.service_method("World")

if __name__ == "__main__":
    logger.info("--------------- server starting....")
    app.run(host='0.0.0.0', port=5000, debug=False)