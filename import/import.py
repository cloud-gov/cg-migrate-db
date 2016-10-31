import sys
import json
import os
import http.server
import socketserver

def find_s3_bucket_creds(vcap):
    s3 = vcap['s3'][0]['credentials']
    return s3['access_key_id'], s3['secret_access_key'], s3['bucket']

def restore_mysql_from_s3(creds, vcap):
    access, secret, bucket = find_s3_bucket_creds(vcap)
    command = 'AWS_ACCESS_KEY_ID="'+access+'" AWS_SECRET_ACCESS_KEY="'+secret+'" bin/gof3r get -b '+bucket+ ' -k db.sql | bin/mysql -u ' + creds['username'] + ' -p' + creds['password']+ ' -h ' + creds['host'] + ' ' + creds['db_name']
    #command = 'bin/mysqldump -u ' + creds['username'] + ' -p' + creds['password']+ ' -h ' + creds['host'] + ' ' + creds['db_name'] + ' | AWS_ACCESS_KEY_ID="'+access+'" AWS_SECRET_ACCESS_KEY="'+secret+'" bin/aws s3 cp - s3://'+bucket+'/db.sql'
    os.system(command)

def importData():
    if os.environ['VCAP_SERVICES']:
        vcap = json.loads(os.environ.get('VCAP_SERVICES'))
        services = vcap['aws-rds']
        for service in services:
            if service['name'] == os.environ.get('TARGET_SERVICE'):
                creds = service['credentials']
                plan = service['plan']
                if "mysql" in plan:
                    if 's3' in vcap:
                        print("found bound s3 bucket. will try to import from s3 bucket")
                        restore_mysql_from_s3(creds, vcap)
                    return
                else:
                    print("Unable to decide how to backup plan: " + plan + ". Exiting.")
                    sys.exit(1)
    print("Unable to do backup")
    sys.exit(2)

importData()
# Create a server in order to download the files.
PORT = int(os.getenv('PORT', '8000'))

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
