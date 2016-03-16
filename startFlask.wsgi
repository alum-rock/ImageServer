#!/usr/bin/python

import sys, os
sys.path.insert (0,'/var/www/ImageServer')
os.chdir("/var/www/ImageServer")
from main import app as application
