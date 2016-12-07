import requests

from flask import render_template, Blueprint

from app.channels import ChannelBase

# todo: make a blueprint so that we can specify the templates folder?
class TestChannel(ChannelBase):
    
    def __init__(self):
        super(TestChannel, self).__init__()

    def render(self):
        html = '<p>This is a test channel. Currently it is quite sad. :(</p>'
        html = html.decode('utf-8')
        return render_template("test_channel.html", **locals())
