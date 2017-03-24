#log to stderr instead of stdout

activate_this = '/opt/dashboard/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import logging, sys
logging.basicConfig(stream=sys.stderr)

import sys
import os

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, path)

from dotenv import load_dotenv
load_dotenv('/opt/dashboard/dashboard/params.env')

from app import app as application
