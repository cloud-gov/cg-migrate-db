#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
import http.server
import socketserver

if os.environ['VCAP_SERVICES']:
    vcap = json.loads(os.environ.get('VCAP_SERVICES'))
    creds = vcap['aws-rds'][0]['credentials']
    command = 'bin/mysqldump -u ' + creds['username'] + ' -p' + creds['password'] + ' -h ' + creds['host'] + ' ' + creds['db_name'] + ' > db.sql'
    #print(command)
    os.system(command)

# Create a server in order to download the files.
PORT = int(os.getenv('PORT', '8000'))

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
