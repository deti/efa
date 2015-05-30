__author__ = 'deti'
"""
API & documentation
https://github.com/toggl/toggl_api_docs
https://dev.evernote.com/doc/start/python.php

https://dev.evernote.com/doc/reference/
https://dev.evernote.com/doc/
"""
import conf
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import urljoin
from datetime import datetime, timedelta
import pytz
import iso8601
from functools import wraps
from tabulate import tabulate

def config_logging():
    import os
    if not os.path.exists(conf.logging.log_dir):
        os.mkdir(conf.logging.log_dir)
    logging.basicConfig(filename=conf.logging.log_file,
                        format=conf.logging.format,
                        level=conf.logging.level)


def debug_decorator(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        logging.debug("{} called".format(func.__name__))
        result = func(*args, **kwargs)
        log_str = "{} finished".format(func.__name__)
        if result:
            log_str = "{}. Result: {}".format(log_str, result)
        logging.debug(log_str)
        return result
    return func_wrapper



@debug_decorator
def start_efa():
    """
    Get all information from Toggle service
    :return:
    """
    print ("Hello world")



def main():
    config_logging()
    print ("efa 3")
    # config_tz()
    logging.info("-------- Start {} --------".format(conf.app_name))
    print ("efa 4")
    start_efa
    logging.info("-------- Finish {} -------".format(conf.app_name))
    print ("efa 5")

if __name__=="__main__":
    print ("efa 1")
    main()
    print ("efa 2")


