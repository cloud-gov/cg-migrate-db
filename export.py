#!/usr/bin/env python3                                                                                                                                                                                                                   
#  -*- coding: utf-8 -*-
import sys
import json
import os

if os.environ['VCAP_SERVICES']:
    vcap = json.loads(os.environ.get('VCAP_SERVICES'))
    creds = vcap['aws-rds'][0]['credentials']
    command = 'mysqldump -u ' + creds['username'] + ' -p' + creds['password'] + ' -h ' + creds['host'] + ' ' + creds['db_name'] + ' > db.sql'
    print(command)
    #os.system(command) 
