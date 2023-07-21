#!/bin/bash

# this may later become an RPM or something IDK


./genginx.py kdlp.ini > kdlp.conf

# move this to /etc/nginx
# mv kdlp.conf /etc/nginx/conf.d

# need to modify nginx main conf too

# restorecon -Rv /etc/nginx/
# nginx -s reload


# dnf install pip python-devel
#


