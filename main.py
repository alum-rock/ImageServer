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

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from pymongo import MongoClient
import pymongo
import sys

app = Flask(__name__)
connection = MongoClient("localhost", serverSelectionTimeoutMS=5000)

try:
    connection.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    print "Unable to connect to database, exiting"
    print(err)
    sys.exit(1)

@app.route('/')
def index():
    return "Welcome to the ImageServer"


if __name__ == '__main__':
    app.run(debug=True)

