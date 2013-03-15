#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:fdm=marker:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import sys, socket, os, errno

if len(sys.argv) < 2:
    print("Must provide at least one argument.", file=sys.stderr)
    raise SystemExit(1)

platform = sys.platform.lower()
use_filesystem = 'darwin' in platform
# use_filesystem = True
del platform

address = ('/tmp/powerline-ipc-%d' if use_filesystem else '\0powerline-ipc-%d')%os.getuid()

sock = socket.socket(family=socket.AF_UNIX)

def eintr_retry_call(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except EnvironmentError as e:
            if getattr(e, 'errno', None) == errno.EINTR:
                continue
            raise

try:
    eintr_retry_call(sock.connect, address)
except Exception:
    # Run the powerline client
    getcwd = getattr(os, 'getcwdu', os.getcwd)
    args = ['powerline'] + sys.argv[1:]
    os.execvp('powerline', args)

fenc = sys.getfilesystemencoding() or 'utf-8'
if fenc == 'ascii':
    fenc = 'utf-8'

cwd = os.getcwd()
if isinstance(cwd, type('')):
    cwd = cwd.encode(fenc)

args = [x.encode(fenc) if isinstance(x, type('')) else x for x in sys.argv[1:]]
args.append(b'--cwd='+cwd)

EOF = b'\0\0'

for a in args:
    eintr_retry_call(sock.sendall, a+EOF[0])

eintr_retry_call(sock.sendall, EOF)

received = []
while True:
    r = sock.recv(4096)
    if not r:
        break
    received.append(r)

sock.close()

print (b''.join(received))

