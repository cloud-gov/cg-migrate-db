#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
from common import *

def find_s3_bucket_creds():
    s3 = json.loads(os.environ.get('STORE_CREDENTIALS'))
    if 'region' in s3:
        return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], s3['region']
    return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], ''

def restore_mysql_from_s3(creds):
    access, secret, bucket, region = find_s3_bucket_creds()
    s3_cmd = build_s3_get_command(access, secret, region, bucket)
    mysql_cred = build_mysql_cred_str(creds)
    command = '{} | bin/mysql {}'.format(s3_cmd, mysql_cred)
    os.system(command)

def restore_psql_from_s3(creds):
    access, secret, bucket, region = find_s3_bucket_creds()
    s3_cmd = build_s3_get_command(access, secret, region, bucket)
    psql_cred = build_psql_env(creds)
    command = '{} | {} bin/pg_restore --format=custom'.format(s3_cmd, psql_cred)
    os.system(command)

def import_data():
    if os.environ['VCAP_SERVICES']:
        vcap = json.loads(os.environ.get('VCAP_SERVICES'))
        services = vcap['aws-rds']
        for service in services:
            if service['name'] == os.environ.get('TARGET_SERVICE'):
                creds = service['credentials']
                plan = service['plan']
                if 's3' in os.environ.get('STORE_TYPE'):
                    if "mysql" in plan:
                        print("found bound s3 bucket and mysql database. will try to import from s3 bucket")
                        restore_mysql_from_s3(creds)
                    elif "psql" in plan:
                        print("found bound s3 bucket and psql database. will try to import from s3 bucket")
                        restore_psql_from_s3(creds)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)
setup()
import_data()
run_server()

