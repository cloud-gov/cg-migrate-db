#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import os
import http.server
import socketserver
import subprocess
import sys
import shutil

def build_psql_env(creds, cmd):
    return 'PGPASSWORD="{}" {} -h "{}" -d "{}" -U "{}"'.format(creds['password'], cmd, creds['host'], creds['db_name'], creds['username'])

def build_mysql_cred_str(creds):
    return '-u {} -p{} -h {} {}'.format(creds['username'], creds['password'], creds['host'], creds['db_name'])

def build_redis_cred_str(creds):
    return '-p {} -h {} -a {}'.format(creds['port'], creds['hostname'], creds['password'])


def build_s3_copy_command(access, secret, region, bucket):
    aws = get_aws_cli_location()
    env = build_aws_env_var(access, secret, region)
    return '{} {} s3 cp - s3://{}/db.sql'.format(env, aws, bucket)

def build_s3_get_command(access, secret, region, bucket):
    aws = get_aws_cli_location()
    env = build_aws_env_var(access, secret, region)
    return '{} {} s3 cp s3://{}/db.sql -'.format(env, aws, bucket)

# get the env vars filled with the appropriate AWS credentials
def build_aws_env_var(access, secret, region):
    env = 'AWS_ACCESS_KEY_ID="{}" AWS_SECRET_ACCESS_KEY="{}"'.format(access, secret)
    if region != '':
        env = '{} AWS_DEFAULT_REGION="{}"'.format(env, region)
    return env

# check for various locations of aws
def get_aws_cli_location():
    if os.path.isfile("/home/vcap/bin/aws"):
        return "/home/vcap/bin/aws"
    elif os.path.isfile("/home/vcap/app/bin/aws"):
        return "/home/vcap/app/bin/aws"
    path = shutil.which("aws")
    if path is not None:
        return path
    return "aws"

# run the command in the shell.
def run_command(cmd, ignore_ret=False):
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as execout:
        if not ignore_ret:
            print("error code", execout.returncode, execout.output)
            sys.exit(1)

# start a web server
def run_server():
    # Create a server in order to download the files.
    PORT = int(os.getenv('PORT', '8000'))

    Handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("serving at port", PORT)
    httpd.serve_forever()