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
from functools import wraps

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore

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

def client():
    """
    :return: client object. On first call esteblish connection and save in conf
    """
    if not hasattr(conf, "_client"):
        conf._client = EvernoteClient(token=conf.evernote.auth_token,
                                      sandbox=conf.evernote.sandbox)
    return conf._client


@debug_decorator
def get_notebooks():
    """
    Call Evernote for notebooks and filter only needed ones
    :return: List of Notebooks objects with names listed in evernote.notebooks
    """
    notebooks = list()
    noteStore = client().get_note_store()
    got_notebooks = noteStore.listNotebooks()
    for n in got_notebooks:
        if n.name in conf.evernote.notebooks:
           notebooks.append(n)
    return notebooks


@debug_decorator
def start_efa():
    """
    Call for Evernote
    :return:
    """
    notebooks = get_notebooks()




def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    start_efa()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


