'''
Created on 2014. 11. 3.

@author: Bong-Jin Kwon
'''
from flask import Flask
import logging
import BongLoggingTest
import BongService


BongLoggingTest.setup_logging();
logger = logging.getLogger(__name__)

app = Flask(__name__)

logging.info("--------------- server starting....")

@app.route("/")
def hello():
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    return BongService.service_method("World")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)