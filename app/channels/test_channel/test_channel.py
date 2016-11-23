import requests

from flask import render_template

from app.channels import ChannelBase


class TestChannel(ChannelBase):
    
    def __init__(self):
        super(TestChannel, self).__init__()

    def render(self):
        html = 'Random Content'
        html = html.decode('utf-8')
        return render_template("test_channel.html", **locals())
    