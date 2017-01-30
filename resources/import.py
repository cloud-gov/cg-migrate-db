#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
from common import *

# for import, we assign the s3 credentials to an environment variable (vs with export, we use the bound service)
# this allows for us to use a s3 bucket in another environment by just putting the credentials in the env vars.
def find_s3_bucket_creds():
    s3 = json.loads(os.environ.get('STORE_CREDENTIALS'))
    if 'region' in s3:
        return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], s3['region']
    return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], ''

# use mysql to restore the database and stream into the database.
def restore_mysql(creds, store_stream_cmd):
    mysql_cred = build_mysql_cred_str(creds)
    command = '{} | bin/mysql {}'.format(store_stream_cmd, mysql_cred)
    run_command(command)

# use pg_restore to restore the database and stream into the database.
def restore_psql(creds, store_stream_cmd):
    psql_cred = build_psql_env(creds, 'bin/pg_restore --format=custom -c')
    command = '{} | {}'.format(store_stream_cmd, psql_cred)
    run_command(command)

# use rutil to restore a redis instance.
def restore_redis(creds, store_stream_cmd):
    redis_cred = build_redis_cred_str(creds)
    command = '{} | bin/rutil {} restore -d -i'.format(store_stream_cmd, redis_cred)
    run_command(command)

def import_data():
    if os.environ['VCAP_SERVICES']:
        vcap = json.loads(os.environ.get('VCAP_SERVICES'))
        services = vcap.get('aws-rds', []) + vcap.get('rds', []) + vcap.get('redis28-swarm', []) + vcap.get('redis28', [])
        for service in services:
            if service['name'] == os.environ.get('TARGET_SERVICE'):
                creds = service['credentials']
                plan = service['plan']
                label = service['label']
                if 's3' in os.environ.get('STORE_TYPE'):
                    access, secret, bucket, region = find_s3_bucket_creds()
                    s3_cmd = build_s3_get_command(access, secret, region, bucket)
                    if "mysql" in plan:
                        print("found bound s3 bucket and mysql database. will try to import from s3 bucket")
                        restore_mysql(creds, s3_cmd)
                    elif "psql" in plan:
                        print("found bound s3 bucket and psql database. will try to import from s3 bucket")
                        restore_psql(creds, s3_cmd)
                    elif "redis28" in label:
                        print("found bound s3 bucket and redis database. will try to import from s3 bucket")
                        restore_redis(creds, s3_cmd)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)
import_data()
run_server()

