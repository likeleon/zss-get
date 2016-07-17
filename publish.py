#!/usr/bin/env python

import subprocess

subprocess.call('python setup.py bdist_egg upload --quiet')
subprocess.call('python setup.py bdist_wininst register upload --quiet')
subprocess.call('python setup.py sdist upload --quiet')
