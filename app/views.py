import json

from flask.ext.classy import FlaskView, route
from flask import render_template, request
from flask import session

from app.channels import render_channel
from app.controller import DashboardController

from app import app

class DashboardView(FlaskView):

    def __init__(self):
        self.base = DashboardController()
        pass

    def before_request(self, name, *args, **kwargs):
        """
        :param name: the name of the function that will be called
        :param args: Any arguments that will be passed to the view.
        :param kwargs: Any keyword arguments that will be passed to the view.
        """

    def index(self):
        title, tab_results = self.base.render_tab(1) # currently this is just using 1 as the id. later, this should use tab_order
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    @route('/tab/<tab_name>')
    def test(self, tab_name):
        title, tab_results = self.base.render_tab(tab_name)  # currently this is just using 1 as the id. later, this should use tab_order
        tabs = self.base.get_tabs()

        return render_template('tab_render.html', **locals())

    def clear_db(self):
        self.base.db_controller.clear_db_generated_content()
        return 'done'

    # todo: this should be cached for a given user at some point
    @route("/render_channel/", methods=['POST'])
    def render_channel(self):

        channel = json.loads(request.data).get('channel')
        channel_class_name = json.loads(channel).get('channel_class_name')
        channel_output = render_channel(channel_class_name)

        return channel_output
