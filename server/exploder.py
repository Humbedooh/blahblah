"""
exploder.py: Handles exploding a list into recipients as well as editing recipient lists
"""
import time
import sys
import threading
import glob
import os
import re
from threading import Lock
from server.threads import fileLock
from server.config import cconfig as config

def list_exists( listname):
    """
    Expands a list name into a file path and returns the file path if it exists, otherwise None
    """
    root = config.get('ListServer', 'listdir')
    bobs = re.split(r"[.@]+", str(listname))
    bobs.reverse()
    listpath = "%s/%s" % (root, "/".join(bobs))
    print("Checking %s..." % listpath)
    if os.path.isdir(listpath):
        return listpath
    else:
        return None
    
    
def get_recipients(listname):
    """
    Opens a recipients file, reads the recips and strips whitespace
    returns as an array of recips if the list can be opened, otherwise an empty array
    """
    fileLock.acquire()
    recips =[]
    try:
        with open("%s/recipients" % listname) as listfile:
            recips = [line.strip() for line in listfile.readlines()]
            listfile.close()
    except Exception as err:
        pass
    fileLock.release()
    return recips

def add_recipient(listname, recipient):
    recips = get_recipients(listname)
    recips.append(recipient)
    fileLock.acquire()
    with open("%s/recipients" % listname, "w") as listfile:
        listfile.write("\n".join(recips))
        listfile.close()
    fileLock.release()
    
    
def remove_recipient(listname, recipient):
    recips = get_recipients(listname)
    try:
        recips.remove(recipient)
    except:
        pass
    fileLock.acquire()
    with open("%s/recipients" % listname, "w") as listfile:
        listfile.write("\n".join(recips))
        listfile.close()
    fileLock.release()