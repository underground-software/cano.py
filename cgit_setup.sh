#!/bin/bash
#
# run when server is running

cd $(dirname $0)

# keep html copy of index for cgit -- yes this is hardcoded FIXME
uwsgi_curl 127.0.0.1:9093 > index.html
sed -e '1,3d' -i index.html

./make_cgitrc.py
cp cgitrc /etc/cgitrc
