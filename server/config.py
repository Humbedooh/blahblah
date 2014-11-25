import configparser
import sys
import os

cconfig = None
mconfig = None


cconfig = configparser.RawConfigParser()
cconfig.read("config/chicken.cfg")

mconfig = configparser.RawConfigParser()
mconfig.read("config/farmer.cfg")