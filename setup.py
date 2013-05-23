#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import,
						print_function)

__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

import sys
import subprocess
from setuptools import setup


def compile():
	# Try to compile the C powerline-client
	if hasattr(sys, 'getwindowsversion'):
		raise NotImplementedError()
	else:
		from distutils.ccompiler import new_compiler
		compiler = new_compiler().compiler
		subprocess.check_call(compiler + ['-O3', 'powerline-client.c', '-o', 'powerline-client'])

try:
	compile()
except Exception:
	import shutil
	print ('Compiling C version of powerline-client failed, using python version')
	shutil.copyfile('powerline-client.py', 'powerline-client')

setup(
	name='powerline-daemon',
	version='1.0',
	description='Daemon to speed up powerline',
	author='Kovid Goyal',
	author_email='kovid@kovidgoyal.net',
	scripts=['powerline-daemon', 'powerline-client']
)
