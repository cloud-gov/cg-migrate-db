#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
import os.path
from common import *

def backup_mysql_to_s3(creds, vcap):
    access, secret, bucket, region = find_s3_bucket_creds(vcap)
    s3_cmd = build_s3_copy_command(access, secret, region, bucket)
    mysql_cred = build_mysql_cred_str(creds)
    command = 'bin/mysqldump {} | {}'.format(mysql_cred, s3_cmd)
    os.system(command)

def backup_psql_to_s3(creds, vcap):
    access, secret, bucket, region = find_s3_bucket_creds(vcap)
    s3_cmd = build_s3_copy_command(access, secret, region, bucket)
    psql_cred = build_psql_env(creds)
    command = '{} bin/pg_dump --format=custom | {}'.format(psql_cred, s3_cmd)
    os.system(command)

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
                    if "mysql" in plan:
                        print("found bound s3 bucket and mysql database. will try to export to s3 bucket")
                        backup_mysql_to_s3(creds, vcap)
                    if "psql" in plan:
                        print("found bound s3 bucket and psql database. will try to export to s3 bucket")
                        backup_psql_to_s3(creds, vcap)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)

setup()
backup()
run_server()
