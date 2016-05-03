#!/usr/bin/python

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# www.github.com/alum-rock/ImageServer

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, send_file
from pymongo import MongoClient
import pymongo
import sys
import ConfigParser
import gridfs
import argparse
import cStringIO
import mimetypes
import requests
import base64
from PIL import Image

CONFIG_FILE = '/etc/ImgSrv.conf'
TEST_IMG = '/tmp/forest.jpg'
HOST = 'localhost'
PORT = 27017

app = Flask(__name__)


# Config file reading
Config = ConfigParser.ConfigParser()

Config.read(CONFIG_FILE)
dbuser = Config.get('Login','username')
dbpwd  = Config.get('Login','password')

# Database connectivity 
connection = MongoClient(HOST, serverSelectionTimeoutMS=5000)
#connection.admin.authenticate(dbuser, dbpwd, mechanism='SCRAM-SHA-1')
#mongo_con = Connection(HOST , PORT)
grid_fs = gridfs.GridFS(connection.grid_database)

try:
    connection.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print "Unable to connect to database, exiting"
    print(err)
    sys.exit(1)

@app.route('/')
def first():
    #db = connection.images
    #output = db.items.find()

    filename = 'testjpeg.jpg'
    stream = grid_fs.get_last_version(filename)
    image = Image.open(stream)
    img_io = cStringIO.StringIO()
    image.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    imgStr = base64.b64encode(img_io.getvalue())
    
#    return send_file(img_io, mimetype='image/jpeg')
    img_tag = '<img src="data:image/png;base64,{0}" height="500">'.format(imgStr)
    toReturn = '<html>'
    toReturn += '<body>'
    toReturn += '<title>ImageServer</title>'
    toReturn += '<center>'
    toReturn += '<strong>Welcome to the ImageServer</strong>'
    toReturn += '</center>'
    toReturn += '<br />'
    toReturn += '<br />'
    toReturn += '<center>'
    toReturn += 'Serving Image from Database'
    toReturn += '</center>'
    toReturn += '<br />'
    toReturn += '<br />'
    toReturn += '<center>'
    toReturn += img_tag
    toReturn += '</center>'
    toReturn += '</body>'
    toReturn += '</html>'
    return toReturn

@app.route('/index')
def index():
    return "Welcome to the ImageServer index"

#@app.route('/image/<path:filename>')
#def get_image(filename):
#    """retrieve an image from mongodb gridfs"""
#
#    if not grid_fs.exists(filename=filename):
#        raise Exception("mongo file does not exist! {0}".format(filename))
#
#    im_stream = grid_fs.get_last_version(filename)
#    im = Image.open(im_stream)
#    return serve_pil_image(im)

@app.route('/addimg')
def add_image():
    filename = 'testjpeg.jpg'
    mimetype='image/jpeg'
    img = Image.open(TEST_IMG)
    img_io = cStringIO.StringIO()
    img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    id = grid_fs.put(img_io, contentType=mimetype, filename=filename)
    return "created file"


@app.route('/getimg')
def get_image():
    filename = 'testjpeg.jpg'
    stream = grid_fs.get_last_version(filename)
    image = Image.open(stream)
    img_io = cStringIO.StringIO()
    image.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    imgStr = base64.b64encode(img_io.getvalue())
    
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/showimg')
def show_image():
    filename = 'testjpeg.jpg'
    mimetype='image/jpeg'
    img = Image.open(TEST_IMG)
    img_io = cStringIO.StringIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
