#!/bin/env python3

from subprocess import run, PIPE
from configparser import ConfigParser
import sys

ini_file='kdlp.ini'
if len(sys.argv) > 1:
    ini_file = sys.argv[1]


parser = ConfigParser()
parser.read(ini_file)
planets = parser['planets']

for planet in planets:
    setup = parser[planet].get('setup', None)
    if setup is None:
        print("No setup for %s" % planet)
        continue

    script_path = "%s/%s"  % (planet, setup)
    print("Running %s..." % script_path)


    out = run(script_path, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print("out: %s" % out.stdout)
    print("\t(ret = %d)" % (out.returncode))
