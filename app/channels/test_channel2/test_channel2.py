import requests

from flask import render_template, Blueprint

from app.channels import ChannelBase

# todo: make a blueprint so that we can specify the templates folder?
class TestChannel2(ChannelBase):
    
    def __init__(self):
        super(TestChannel2, self).__init__()

    def render(self):
        # TestChannelModel()
        # todo: we need db_session
        # todo: we need to access the channel options

        html = 'This is a test channel. Currently it is quite sad. :('
        html = html.decode('utf-8')
        return render_template("test_channel2.html", **locals())
