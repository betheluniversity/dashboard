from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from importlib import import_module
import os

from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# import all models
from app.models import *

# Get all channel models
channels_folder = os.path.dirname(os.path.realpath(__file__)) + "/app/channels"
for root, dirs, files in os.walk(channels_folder):
    for d in dirs:
        import_module('app.channels.' + d + '.models')

if __name__ == '__main__':
    manager.run()
