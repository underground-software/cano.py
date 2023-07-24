#!/bin/bash

# this may later become an RPM or something IDK


# dnf install nginx sqlite

./genginx.py kdlp.ini > kdlp.conf

# move this to /etc/nginx
# mv kdlp.conf /etc/nginx/conf.d

# need to modify nginx main conf too
# easy solution: swap out config with our own
#cp /etc/nginx/nginx.conf nginx.conf.bak
#cp nginx.conf.orbit /etc/nginx/nginx.conf

# systemctl start nginx
#
# important: restore selinux labels and reload nginx
#restorecon -Rv /etc/nginx/
#nginx -s reload
#
# maybe need this one too?
setsebool -P httpd_can_network_connect 1
# found with audit2why


# dnf install pip python-devel

# pip install -r requirements.txt

./gather_planets.py

# run pip install -r requirements.txt in each repo
# honestly maybe run a 'setup.sh' in each on (based on config?)
# TODO
#
# cgit setup

dnf install cgit fcgiwrap
