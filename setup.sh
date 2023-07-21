#!/bin/bash

# this may later become an RPM or something IDK


./genginx.py kdlp.ini > kdlp.conf

# move this to /etc/nginx
# mv kdlp.conf /etc/nginx/conf.d

# need to modify nginx main conf too
# easy solution: swap out config with our own
#cp /etc/nginx/nginx.conf nginx.conf.bak
#cp nginx.conf.orbit /etc/nginx/nginx.conf

# important: restore selinux labels and reload nginx
#restorecon -Rv /etc/nginx/
#nginx -s reload


# dnf install pip python-devel
#

./gather_planets.py

# run pip install -r requirements.txt in each repo
# honestly maybe run a 'setup.sh' in each on (based on config?)
