#!/bin/env python3

import os, sys
from configparser import ConfigParser
from git import Repo
from orbit import DP

START_TEMPLATE="""
[uwsgi]
socket = localhost:%(port)s
chdir = %(dir)s
wsgi-file = app.py
processes = 4
threads = 2
""".strip()

# skip anything with stats server for now

# quick and dirty: load authority server from auth_server file generated by genginx.py
auth_server=''
try:
    with open('auth_server', 'r') as f:
        auth_server = f.read()
except:
    DP('no auth_server file found? Run genginx.py first or create it manually')

ini_file='kdlp.ini'
if len(sys.argv) > 1:
    ini_file = sys.argv[1]

parser = ConfigParser()
parser.read(ini_file)
planets = parser['planets']

for planet in planets:
    if os.path.exists(planet):
        print(f'##### SKIPPING {planet} BECAUSE IT ALREADY EXISTS #####')
        continue
    _plan = parser[planet]
    config = ''

    ver = _plan.get('ver')
    source = planets[planet]
    print('##### GATHER %s %s %s ######' % (planet, ver, source))

    config += "APPLICATION = '%s'\n" % planet
    config += "VERSION = '%s'\n" % ver
    config += "SOURCE = '%s'\n" % source

    # don't bother with version until this stabilizes
    repo = Repo.clone_from(source, planet)
    repo.head.reference = repo.create_head(ver, ver)
    repo.head.reset(index=True, working_tree=True)

    config += "ROOT = '%s'\n" % (os.getcwd() + '/root')
    config += "AUTH_SERVER = '%s'\n" % auth_server
    # here we would check out the right version but don't bother for now

    # install the new config and common library
    with open('orbit.py', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('###@REPLACE@###', config)

    with open(planet + '/orbit.py', 'w') as file:
        file.write(filedata)

    start_ini = START_TEMPLATE % {
            "port": _plan.get('port'),
            "dir": "%s/%s" % (os.getcwd(), planet)}
    # bad hack to make auth server run over http
    # should not hardcode this but I'm doing it anyway for now
    # FIXME
    if planet == 'venus':
        start_ini = start_ini.replace('socket', 'http')
    with open(planet + '/start.ini', 'w') as file:
        file.write(start_ini)

if os.path.exists('root'):
    print(f'##### SKIPPING root BECAUSE IT ALREADY EXISTS #####')
    exit()

root = parser['root']
root_source = root.get('source')
root_ver = root.get('ver')

print('##### root %s %s #####' % (root_ver, root_source))

repo = Repo.clone_from(root_source, 'root')
repo.head.reference = repo.create_head(root_ver, 'origin/' + root_ver)
repo.head.reset(index=True, working_tree=True)

