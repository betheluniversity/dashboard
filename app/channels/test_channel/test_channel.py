import requests

from flask import render_template, Blueprint, session

from app.channels import ChannelBase
from app.channels.test_channel.models import TestChannelOptions
from app.models import User
from app.db_controller import DBController

from app import db

# todo: make a blueprint so that we can specify the templates folder?
class TestChannel(ChannelBase):

    def __init__(self):
        super(TestChannel, self).__init__()
        self.DBController = DBController()

    def render(self):
        db_session = db.session
        options = db_session.query(User, TestChannelOptions) \
            .join(TestChannelOptions) \
            .filter(User.username == session['username']) \
            .all()

        try:
            color = options[0].TestChannelOptions.color
        except:
            new_option = TestChannelOptions(self.DBController.get_current_users_id(), 'lightblue')
            db_session.add(new_option)
            db_session.commit()
            color = new_option.color

        import random
        if random.randint(1, 10) == 1:
            raise Exception('test')

        html = 'This is a test channel. Currently it is quite sad. :( However, this color you see is gotten from the dashboad_test_channel table! yay.'
        html = html.decode('utf-8')
        return render_template("test_channel.html", **locals())
