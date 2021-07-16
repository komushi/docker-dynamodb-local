#! /usr/bin/env python3

import os
import subprocess
import xml.etree.ElementTree as ET

import requests
import shutil


DDB_BUCKET_URL = 'https://s3-us-west-2.amazonaws.com/dynamodb-local/'


req = requests.get(DDB_BUCKET_URL)
root = ET.fromstring(req.text)

keys = [key.text for content in root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents')
        for key in content.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Key')
        if key.text.endswith('.tar.gz')]
print(keys)

dockerfile = open('Dockerfile.debian9.tpl').read()
entrypoint = open('docker-entrypoint.sh').read()
for key in keys:
    version = key.replace('dynamodb_local_', '').replace('.tar.gz', '')
    print('Key = ' + key + ', version = ' + version)
    if version == 'latest' or version < '2021-04-27' or version.startswith('test'):
        # Ignore older versions
        # *.tar.gz.sha256 is not available for versions older than 2016-04-19
        continue
    try:
        os.mkdir(version)
    except:
        pass
    new_dockerfile = dockerfile.replace('latest', version)
    open(os.path.join(version, 'Dockerfile'), 'w').write(new_dockerfile)
    open(os.path.join(version, 'docker-entrypoint.sh'), 'w').write(entrypoint)
    os.chmod(os.path.join(version, 'docker-entrypoint.sh'), 0o755)
    shutil.copy('./armv7lib/libsqlite4java-linux-arm.so.debian9', os.path.join(version, 'libsqlite4java-linux-arm.so'))
    #shutil.copy('./armv7lib/intarray.o', os.path.join(version, 'intarray.o'))
    #shutil.copy('./armv7lib/sqlite_wrap.o', os.path.join(version, 'sqlite_wrap.o'))
    #shutil.copy('./armv7lib/sqlite3_wrap_manual.o', os.path.join(version, 'sqlite3_wrap_manual.o'))
    #shutil.copy('./armv7lib/sqlite3.o', os.path.join(version, 'sqlite3.o'))

# build
# for d in os.listdir('.'):
#     if os.path.isdir(d) and not d.startswith('.'):
#         print ('Working on ' + d)
#         subprocess.call(
#             ['docker', 'build', '--tag', 'komushi/dynamodb-local-alpine:' + d, d])
