from flask.ext.classy import FlaskView, route
from flask import render_template

from app import app

class DashboardView(FlaskView):

    def __init__(self):
        pass

    def before_request(self, name, *args, **kwargs):
        """
        :param name: the name of the function that will be called
        :param args: Any arguments that will be passed to the view.
        :param kwargs: Any keyword arguments that will be passed to the view.
        """

    def index(self):
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        return render_template('base.html', **locals())

    @route('/testing/<num>')
    def test(self, num):
        return "test %s" % num
