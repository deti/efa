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
from xml.dom import minidom
from sqlitedict import SqliteDict

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore

def config_logging():
    import os
    if not os.path.exists(conf.logging.log_dir):
        os.mkdir(conf.logging.log_dir)
    logging.basicConfig(filename=conf.logging.log_file,
                        format=conf.logging.format,
                        level=conf.logging.level)


def debug_decorator(log_result=True):
    def parametremized_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            logging.debug("{} called".format(func.__name__))
            result = func(*args, **kwargs)
            log_str = "{} finished".format(func.__name__)
            if result and log_result:
                log_str = "{}. Result: {}".format(log_str, result)
            logging.debug(log_str)
            return result
        return func_wrapper
    return parametremized_decorator

def client():
    """
    :return: client object. On first call esteblish connection and save in conf
    """
    if not hasattr(conf, "_client"):
        conf._client = EvernoteClient(token=conf.evernote.auth_token,
                                      sandbox=conf.evernote.sandbox)
    return conf._client


@debug_decorator(log_result=False)
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

@debug_decorator(log_result=False)
def get_notes(notebooks):
    """
    :param notebooks: List of evernote Notebook objects
    :return: List of Notes for passed Notebook
    """
    notes = list()
    for notebook in notebooks:
        filter = NoteStore.NoteFilter()
        filter.notebookGuid = notebook.guid

        noteStore = client().get_note_store()
        step = 50
        start = 0
        note_list = noteStore.findNotes(conf.evernote.auth_token, filter, start, step)
        while note_list.notes:
            notes.extend(note_list.notes)
            start += step
            note_list = noteStore.findNotes(conf.evernote.auth_token, filter, start, step)
    return notes

@debug_decorator(log_result=True)
def adjust_note(note):
    '''
    :param note: Update note style
    '''
    noteStore = client().get_note_store()
    content = noteStore.getNoteContent(conf.evernote.auth_token, note.guid)
    dom = minidom.parseString(content)
    for div in dom.getElementsByTagName("div"):
        div.setAttribute("style", "font-size: {}px; line-height: {}%;"\
                         .format(conf.font_size, conf.line_height))
    note.content = dom.toxml()
    logging.debug("Saving note: {}".format(note.title))
    noteStore.updateNote(conf.evernote.auth_token, note)


FONT_SIZE = "FONT_SIZE"
LINE_HEIGHT = "LINE_HEIGHT"
@debug_decorator(log_result=True)
def adjust_evernote_font():
    """
    Call for Evernote
    """
    note_info = SqliteDict(conf.db.db_file, autocommit=True)

    notes_in_evernote = list()
    for note in get_notes( get_notebooks() ):
        guid = note.guid
        notes_in_evernote.append(guid)
        if guid not in note_info.keys() \
            or note_info[guid][FONT_SIZE] != conf.font_size \
            or note_info[guid][LINE_HEIGHT] != conf.line_height:
            adjust_note(note)
            note_info[guid] = {FONT_SIZE:conf.font_size,
                            LINE_HEIGHT:conf.line_height}

    guids_to_delete = [guid for guid in note_info.keys()
                       if guid not in notes_in_evernote ]

    for to_delete in guids_to_delete:
        logging.debug("Reomoe guid from DB: {}".format(to_delete))
        del note_info[to_delete]

    note_info.close()


def main():
    config_logging()
    logging.info("-------- Start {} --------".format(conf.app_name))
    adjust_evernote_font()
    logging.info("-------- Finish {} -------".format(conf.app_name))

if __name__=="__main__":
    main()


