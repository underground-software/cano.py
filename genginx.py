#!/bin/env python3

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

AUTH_CHECK="""

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
	proxy_pass http://localhost:9090$uri?$query_string;
}
""".strip() + '\n\n'

SPECIAL_NAKED_EXCEPTION="""
location = / {
    rewrite .* /index.md;
}
""".strip() + '\n\n'

def make_nginx_uwsgi_block(location, port, comment, auth=False):
    block = "# " + comment + '\n'
    block += 'location ' + location + ' {\n'
    if auth:
        block += '\tauth_request /auth_check;\n'
    block += '\tinclude uwsgi_params;\n'
    block += '\tuwsgi_pass uwsgi://localhost:' + port + ';\n}\n\n'

    return block

parser = ConfigParser()

parser.read('kdlp.ini')

planets = parser['planets']

def make_nginx_blocks():
    blocks = ""
    for planet in planets:
        _plan = parser[planet]
        ver = _plan.get('ver')
        port = _plan.get('port')
        location = _plan.get('location')
        auth = _plan.getboolean('auth', False)
        #print(planet, ver, auth)

        # could make non-uwsgi block here if config specifies it
        block = make_nginx_uwsgi_block(location, port, str(planet).upper(), auth=auth)
        blocks += block

    return blocks

nginx_config = HEADER + AUTH_CHECK + SPECIAL_NAKED_EXCEPTION + make_nginx_blocks()

print(nginx_config)
