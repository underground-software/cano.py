#!/bin/env python3

from subprocess import run, PIPE
from configparser import ConfigParser

parser = ConfigParser()
parser.read('kdlp.ini')
planets = parser['planets']

for planet in planets:
    setup = parser[planet].get('setup', None)
    if setup is None:
        print("No setup for %s\n", planet)
        continue
    print("Running %s/%s...\n", (planet, setup))

    out = run(['%s/%s' % (planet, setup)], stdout=PIPE, stderr=PIPE)
    print("\t(ret = %d)\n" % (out.returncode))
