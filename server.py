import sys
haveinotify = False
try:
    import pyinotify
    haveinotify = True
    print("Using pyinotify")
except:
    print("pyinotify not available, resorting to polling for config changes :(")

if sys.version_info<(3,0,0):
    print("This nifty piece of software REQUIRES Python 3.0 or newer!")
    sys.exit(-1)
    
# Import dependencies
import json, http.client, urllib.request, urllib.parse, configparser, re, base64, sys, os, time, atexit, signal, logging, subprocess
import socketserver
import threading
from datetime import datetime
import os
from threading import Lock

import server.smtp_incoming as smtpi
import server.config as config


if __name__ == "__main__":
    smtpi.start()
    while True:
        time.sleep(99)