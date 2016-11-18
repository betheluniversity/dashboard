import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config.from_object(os.environ['dashboard_config'])

db = SQLAlchemy(app)

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