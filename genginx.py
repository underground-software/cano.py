#!/bin/env python3
#
# A script to generate an nginx config from our .ini file

import os, sys
from configparser import ConfigParser

HEADER="""
# KDLP Proxy Configuration
# Include in ssl server block in http block

#error_page 401 /401.md;
error_page 401 /unauthorized?target=$uri;
error_page 403 /403.md;
error_page 404 /404.md;
error_page 502 /502.md;
error_page 502 /502.md;
error_page 500 /500.md;
""".strip() + '\n\n'

ROOT_TEMPLATE="""
location / {
    root %s;
}
""".strip() + '\n\n'

AUTH_CHECK_TEMPLATE="""

location /auth_check {
	internal;
	rewrite ^.*$ /check?token=$cookie_auth;
}

location /unauthorized {
	internal;
	rewrite ^.*$ /login?$query_string;
}

location /check {
	internal;

	proxy_pass_request_body off;
	proxy_set_header Content-Length "";

	include uwsgi_params;
	proxy_pass http://localhost:%s$uri?$query_string;
}

location /.well-known/matrix/client {
	return 200 '{"m.homeserver": {"base_url": "https://kdlp.underground.software:8448"}}';
	default_type application/json;
	add_header Access-Control-Allow-Origin *;
}

location = /devfooter {
    internal;
    return 200 "<hr><i><h3>Development Instance</h3> Refreshing every 10 seconds</i><hr><meta http-equiv=\\\"refresh\\\" content=\\\"10\\\">";

}

""".strip() + '\n\n'

SPECIAL_NAKED_EXCEPTION="""
location = / {
    rewrite .* /index.md;
}
""".strip() + '\n\n'

# TODO: un-hardcode this
CGIT_BLOCK="""
# CGIT COMET
location ~* /cgit(.*) {
	include fastcgi_params;

	fastcgi_param SCRIPT_FILENAME /var/www/cgi-bin/cgit;
	fastcgi_param PATH_INFO $1;

	fastcgi_pass localhost:7070;
}
""".strip()


# default to something bad to detect badness more easily
authority_port = "XXXXXX"

# this is slightly confusing, but auth means needs authentication,
# while authority means authentication server
# TODO rename here and in kdlp.ini too

def make_nginx_uwsgi_block(location, port, comment, auth=False, authority=False):
    block = "# " + comment + '\n'
    block += 'location ' + location + ' {\n'
    if auth:
        block += '\tauth_request /auth_check;\n'
    block += '\tinclude uwsgi_params;\n'
    # for development, include the development footer
    block += '\tadd_after_body /devfooter;\n'

    # TEMPORARY: run auth server as http (need to get it working internally with uwsgi)
    if authority:
        block += '\tproxy_pass http://localhost:' + port + ';\n}\n\n'
    else:
        block += '\tuwsgi_pass uwsgi://localhost:' + port + ';\n}\n\n'

    return block

def make_nginx_blocks():
    global authority_port
    blocks = ""
    for planet in planets:
        _plan = parser[planet]
        ver = _plan.get('ver')
        port = _plan.get('port')
        location = _plan.get('location')
        auth = _plan.getboolean('auth', False)
        authority = _plan.getboolean('authority', False)
        if authority:
            authority_port = port

        # could make non-uwsgi block here if config specifies it
        block = make_nginx_uwsgi_block(location, port, str(planet).upper(), auth=auth, authority=authority)
        blocks += block

    return blocks

ini_file='kdlp.ini'
if len(sys.argv) > 1:
    ini_file = sys.argv[1]

parser = ConfigParser()
parser.read(ini_file)
planets = parser['planets']

ROOT = ROOT_TEMPLATE % (os.getcwd() + '/root/data')
blocks = make_nginx_blocks()
AUTH_CHECK = AUTH_CHECK_TEMPLATE % authority_port
# quick and dirty way to pass auth sever around
with open('auth_server', 'w') as file:
    file.write('http://127.0.0.1:%s' % authority_port)

nginx_config = HEADER + ROOT + AUTH_CHECK + SPECIAL_NAKED_EXCEPTION + blocks + CGIT_BLOCK

# just dump it to stdout
print(nginx_config)
