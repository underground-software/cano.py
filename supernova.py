#!/bin/env python3
#
# delete solar system instance -- very simple

import shutil
from configparser import ConfigParser

parser = ConfigParser()
parser.read('kdlp.ini')
planets = parser['planets']

for planet in planets:
    shutil.rmtree(planet)
shutil.rmtree('root')
