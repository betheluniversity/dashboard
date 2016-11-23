from flask.ext.classy import FlaskView, route
from flask import render_template
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
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        username = session['username']

        database = self.base.get_database()

        self.base.db_controller.get_joined_tabs()
        tab = self.base.render_tab(1)
        return render_template('base.html', **locals())

    @route('/testing/<num>')
    def test(self, num):
        return "test %s" % num
