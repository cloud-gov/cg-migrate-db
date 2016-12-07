#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
import os.path
from common import *

# use mysqldump to backup the database and stream the result into a given store.
def backup_mysql(creds, store_stream_cmd):
    mysql_cred = build_mysql_cred_str(creds)
    command = 'bin/mysqldump {} | {}'.format(mysql_cred, store_stream_cmd)
    run_command(command)

# use pg_dump to backup the database and stream the result into a given store.
def backup_psql(creds, store_stream_cmd):
    psql_cred = build_psql_env(creds, 'bin/pg_dump --format=custom')
    command = '{} | {}'.format(psql_cred, store_stream_cmd)
    run_command(command)

# for export, we need to know the bound s3 bucket. for now, just get the first bucket.
def find_s3_bucket_creds(vcap):
    s3 = vcap['s3'][0]['credentials']
    if 'region' in s3:
        return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], s3['region']
    return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], ''

def backup():
    if os.environ['VCAP_SERVICES']:
        vcap = json.loads(os.environ.get('VCAP_SERVICES'))
        services = vcap['aws-rds']
        for service in services:
            if service['name'] == os.environ.get('SOURCE_SERVICE'):
                creds = service['credentials']
                plan = service['plan']
                if 's3' in vcap:
                    access, secret, bucket, region = find_s3_bucket_creds(vcap)
                    s3_cmd = build_s3_copy_command(access, secret, region, bucket)
                    if "mysql" in plan:
                        print("found bound s3 bucket and mysql database. will try to export to s3 bucket")
                        backup_mysql(creds, s3_cmd)
                    if "psql" in plan:
                        print("found bound s3 bucket and psql database. will try to export to s3 bucket")
                        backup_psql(creds, s3_cmd)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)

backup()
run_server()
