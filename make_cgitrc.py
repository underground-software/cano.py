#!/bin/env python3

import os, git, sys
from configparser import ConfigParser

GIT_LOCATION="/var/git"

CGITRC_TEMPLATE="""
# Specify the css url
css=/style.css

# Allow http transport git clone
enable-http-clone=1

# Enable caching of up to 1000 output entries
cache-size=1000

# Use a custom logo
logo=/images/kdlp_logo.png

# Set the title and heading of the repository index page
root-title=Kernel Development Learning Pipeline

# Set a subheading for the repository index page
root-desc=KDLP Git repositories

# Include some more info about this site on the index page
root-readme=%(cache)s/index.html

##
## List of common mimetypes
##

mimetype.gif=image/gif
mimetype.html=text/html
mimetype.jpg=image/jpeg
mimetype.jpeg=image/jpeg
mimetype.pdf=application/pdf
mimetype.png=image/png
mimetype.svg=image/svg+xml

virtual-root=/cgit

scan-path=%(scan_path)s
""".strip()

try:
    os.mkdir(GIT_LOCATION)
except FileExistsError:
    # It's fine if the location already exists
    pass

ini_file='kdlp.ini'
if len(sys.argv) > 1:
    ini_file = sys.argv[1]

parser = ConfigParser()
parser.read(ini_file)
cgit = parser['cgit']
repos = cgit['list']

#repo = Repo.clone_from()


CGITRC = CGITRC_TEMPLATE % {
    "cache": os.getcwd(),
    "scan_path": GIT_LOCATION
}

repolist=""
with open(repos) as f:
    repolist=f.read().strip()

for r in repolist.split('\n'):
    target = "%s/%s" % (GIT_LOCATION, os.path.basename(r))
    print("check", target)
    if not os.path.isdir(target):
        git.Repo.clone_from(r, target)

with open('cgitrc', 'w') as f:
    f.write(CGITRC)
