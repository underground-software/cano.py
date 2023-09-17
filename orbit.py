#!/bin/env python3

import requests, os, sys
from http import cookies

# common library

# client app needs
# APPLICATION, VERSION, ROOT, AUTH_SERVER

###@REPLACE@###

def DP(strg):
    print(strg, file=sys.stderr)

def get_token_from_cookie(env):
    # get auth=$TOKEN from user cookie
    cookie_user_raw = env.get('HTTP_COOKIE', '')
    cookie_user = cookies.BaseCookie('')
    cookie_user.load(cookie_user_raw)

    auth = cookie_user.get('auth', cookies.Morsel())
    if auth.value is not None:
        return auth.value

def get_authorized_user(server, env):
    token = get_token_from_cookie(env)
    uri ='%s/check?token=%s' % (AUTH_SERVER, token)

    res = requests.get(uri, verify=False)

    DP('req to uri="%s" returned %s' % (uri, res.status_code))
    DP('content: %s' % res.text)
    
    if res.status_code == 200:
        split=res.text.split('=')
        if len(split) > 0:
            return split[1]

    return None

def appver():
    return "%s %s %s" % (APPLICATION, VERSION, SOURCE)

def messageblock(lst):
    res=''
    sep = '<br /><hr /><br />'

    res += sep
    for item in lst:
        res += "<code>%s = %s</code><br />" % (item[0], str(item[1]))
    res += sep

    return res

def h(v, c):
    return '<h%d>%s</h%d>' % (v, c, v)

def h1(c):
    return h(1, c)

def h2(c):
    return h(2, c)

def h3(c):
    return h(2, c)

def t_i(i):
    return ''.join(['\t' for x in range(i)])

def o(i, c):
    return '%s%s\n' % (t_i(i), c)

def ooo(i, c, d, e, j=0):
    return '%s%s%s' % (o(i, c), o(i+j, d), o(i, e))

def oOo(i, c, d, e):
    return ooo(i, c, d, e, j=1)

def oxo(i, c, d, e):
    return '%s%s%s' % (o(i, c), d, o(i, e))

def table_data(c, h=False, i=0):
    d = 'd'
    if h:
        d = 'h'
    a, b = '<t%s>' % d, '</t%s>' % d
    return oOo(i, a, c, b)

def table_row(c, h=False, i=0):
    d = ''.join([table_data(d, h=h, i=i+1) for d in c])
    return oxo(i, '<tr>', d, '</tr>')

def table(c, i=0):
    t=''
    h=True
    for r in c:
        t += table_row(r, h, i=i+1)
        h=False
    return oxo(i, '<table>', t, '</table>')

def button(c, i=0, a=''):
    return oOo(i, '<button %s>' % a, c, '</button>')

def debug_table(fname):
    tc = [('key', 'value')]
    found =''
    try:
        if os.path.exists(fname):
            tc += [('fname', fname)]
            tc += [('exists', str(True))]
            tc += [('isfile', str(os.path.isfile(fname)))]
            tc += [('isdir', str(os.path.isdir(fname)))]
        else:
            tc += [('fname', fname)]
            tc += [('exists', str(False))]

        if os.path.isdir(fname):
            fname += '/index.md'
            tc += [('isdir =>', fname)]
            tc += [('isfile', str(os.path.isfile(fname)))]
            tc += [('isdir', str(os.path.isdir(fname)))]
            tc += [('exists', str(os.path.exists(fname)))]
    except FileNotFoundEror as e:
        tc += [(fname, 'error')]

    return table(tc)
