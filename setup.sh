#!/bin/bash

# TODO check if we are in /root
if pwd | grep "^/root" > /dev/null; then
	echo "Please don't install this system in /root"
	exit 0
fi

# we may turn this into an RPM

# We need nginx as our reverse proxy and sqlite for our databases
# We need pip and python-devel to run our applications
dnf install -y nginx sqlite pip python-devel

# Install python package requirements
pip install -r requirements.txt

# Generate out nginx configuration
./genginx.py kdlp.ini > kdlp.conf

# move this to /etc/nginx
mv kdlp.conf /etc/nginx/conf.d

# need to modify nginx main conf too
# easy solution: swap out config with our own
cp /etc/nginx/nginx.conf nginx.conf.bak
cp nginx.conf.orbit /etc/nginx/nginx.conf

# restore selinux labels on newly added files and reload nginx
restorecon -Rv /etc/nginx/

# start nginx if not already running, restart if it is running
systemctl is-active --quiet nginx && \
	nginx -s reload || \
	systemctl start gi
# allow 
setsebool -P httpd_can_network_connect 1

# Download the servers and give them the orbit library and start.ini files
./gather_planets.py kdlp.ini

# run setup scripts for individiual apps if specified
./post_gather.py kdlp.ini

# run pip install -r requirements.txt in each repo
# honestly maybe run a 'setup.sh' in each on (based on config?)
# TODO
#
# cgit setup
#
# I'm thinking something like this (in a python script)
# if /var/git doesn't exist, create it
# then based on config, check if certain repos exist
# if they don't, clone them. If they do, update them

dnf install -y cgit fcgiwrap
