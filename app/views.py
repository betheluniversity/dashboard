import json

from flask.ext.classy import FlaskView, route
from flask import render_template, request
from flask import session

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

    # todo: remove this once testing is done
    def clear_db(self):
        self.base.db_controller.clear_db_generated_content()
        return 'done'

    def admin_view(self):
        tabs = self.base.get_tabs()
        column_formats = self.base.db_controller.get_column_formats_values()
        channels = self.base.db_controller.get_all_channels_values()

        return render_template('admin_base.html', **locals())
