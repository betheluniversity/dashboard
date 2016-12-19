from flask.ext.classy import FlaskView, route
from flask import render_template
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

    # TODO: currently this is using a jinja filter. This is to render the channel as needed from the html side,
    # so we don't do it all at once on the python side.
    # this should be cached for a given user at some point
    @app.template_filter('render_channel')
    def render_channel(self):
        # in this case, self is the channel.
        channel_class_name = self.channel_class_name
        channel_output = render_channel(channel_class_name)

        # Todo: we need this to be able to be rendered via ajax

        # todo: we also would love to potentially be able to cache these

        return channel_output
