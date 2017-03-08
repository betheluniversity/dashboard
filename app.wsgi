#log to stderr instead of stdout

activate_this = '/opt/dashboard/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import logging, sys
logging.basicConfig(stream=sys.stderr)

import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)

from dashboard import app as application

