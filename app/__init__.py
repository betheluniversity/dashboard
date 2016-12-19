import os
import jinja2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


_basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config.from_object(os.environ['dashboard_config'])
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(_basedir, 'test.db')
# db.create_all()

# views templates folder. Any folder in app.channels can contain templates
folders = []
channels_folder = os.path.dirname(os.path.realpath(__file__)) + "/channels"
for root, dirs, files in os.walk(channels_folder):
    for d in dirs:
        folders.append("%s/%s" % (channels_folder, d))

portal_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(folders),
    ])
app.jinja_loader = portal_loader

from app.controller import DashboardController
controller = DashboardController()

from app.models import User
admin = Admin(app, name='dashboard', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

from app.views import DashboardView
DashboardView.register(app, route_base='/')


@app.before_request
def before_request():
    controller.before_request()