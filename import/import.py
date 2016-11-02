#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import sys
import json
import os
import http.server
import socketserver

def getAWSBinLocation():
    if os.path.isfile("/home/vcap/bin/aws"):
        return "/home/vcap/bin/aws"
    elif os.path.isfile("/home/vcap/app/bin/aws"):
        return "/home/vcap/app/bin/aws"
    return ""

def find_s3_bucket_creds():
    s3 = json.loads(os.environ.get('STORE_CREDENTIALS'))
    if 'region' in s3:
        return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], s3['region']
    return s3['access_key_id'], s3['secret_access_key'], s3['bucket'], ''

def restore_mysql_from_s3(creds, vcap):
    access, secret, bucket, region = find_s3_bucket_creds()
    aws = getAWSBinLocation()
    if region != '':
        command = 'AWS_DEFAULT_REGION="'+region+'" AWS_ACCESS_KEY_ID="'+access+'" AWS_SECRET_ACCESS_KEY="'+secret+'" ' + aws + ' s3 cp s3://'+bucket+ '/db.sql - | bin/mysql -u ' + creds['username'] + ' -p' + creds['password']+ ' -h ' + creds['host'] + ' ' + creds['db_name']
        os.system(command)
    else:
        command = 'AWS_ACCESS_KEY_ID="'+access+'" AWS_SECRET_ACCESS_KEY="'+secret+'" '+ aws +' s3 cp s3://'+bucket+ '/db.sql - | bin/mysql -u ' + creds['username'] + ' -p' + creds['password']+ ' -h ' + creds['host'] + ' ' + creds['db_name']
        os.system(command)

def install_aws_cli():
    os.system("awscli-bundle/awscli-bundle/install -b ~/bin/aws")
def importData():
    if os.environ['VCAP_SERVICES']:
        vcap = json.loads(os.environ.get('VCAP_SERVICES'))
        services = vcap['aws-rds']
        for service in services:
            if service['name'] == os.environ.get('TARGET_SERVICE'):
                creds = service['credentials']
                plan = service['plan']
                if "mysql" in plan:
                    if 's3' in os.environ.get('STORE_TYPE'):
                        print("found bound s3 bucket. will try to import from s3 bucket")
                        restore_mysql_from_s3(creds, vcap)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)
install_aws_cli()
importData()
# Create a server in order to download the files.
PORT = int(os.getenv('PORT', '8000'))

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
