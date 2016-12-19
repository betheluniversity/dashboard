from flask import session
# from flask import current_app
from flask import request
from flask import render_template
from flask import json as fjson

from bu_cascade.asset_tools import *

import requests

from app.models import *
from app.db_controller import DBController

from app import app


class DashboardController(object):

    def __init__(self):
        self.db_controller = DBController()

    def before_request(self):
        def init_user_session():

            dev = app.config['DEBUG'] == True

            # if not production, then clear our session variables on each call
            if dev:
                for key in ['username', 'groups', 'roles', 'top_nav', 'user_email', 'name']:
                    if key in session.keys():
                        session.pop(key, None)

            if 'username' not in session.keys():
                get_user()

            if 'groups' not in session.keys():
                get_groups_for_user()

            if 'roles' not in session.keys():
                get_roles()

            if 'user_email' not in session.keys() and session['username']:
                # todo, get prefered email (alias) from wsapi once its added.
                session['user_email'] = session['username'] + "@bethel.edu"

            if 'name' not in session.keys() and session['username']:
                get_users_name()

        def get_user():
            if app.config['DEBUG'] == True:
                username = app.config['TEST_USERNAME']
            else:
                username = request.environ.get('REMOTE_USER')

            session['username'] = username

        def get_users_name(username=None):
            if not username:
                username = session['username']
            url = app.config['API_URL'] + "/username/%s/names" % username
            r = requests.get(url)
            try:
                # In some cases, '0' will not be a valid key, throwing a KeyError
                # If that happens, session['name'] should be an empty string so that checks in other locations will fail
                names = fjson.loads(r.content)['0']
                if names['prefFirstName']:
                    fname = names['prefFirstName']
                else:
                    fname = names['firstName']
                lname = names['lastName']
                session['name'] = "%s %s" % (fname, lname)
            except KeyError:
                session['name'] = ""

        def get_groups_for_user(username=None):
            skip = request.environ.get('skip-groups') == 'skip'
            if not username:
                username = session['username']
            if not skip:
                try:
                    user = self.read(username, "user")
                    allowed_groups = find(user, 'groups', False)
                except AttributeError:
                    allowed_groups = ""
            else:
                allowed_groups = ""
            if allowed_groups is None:
                allowed_groups = ""

            session['groups'] = allowed_groups
            return allowed_groups.split(";")

        def get_roles(username=None):
            if not username:
                username = session['username']
            url = app.config['API_URL'] + "/username/%s/roles" % username
            r = requests.get(url, auth=(app.config['API_USERNAME'], app.config['API_PASSWORD']))
            roles = fjson.loads(r.content)
            ret = []
            for key in roles.keys():
                ret.append(roles[key]['userRole'])

            session['roles'] = ret

            return ret

        self.db_controller.clear_db_generated_content()
        self.db_controller.init_db()
        init_user_session()
        self.db_controller.create_new_user()

    def render_tab(self, tab_order_or_tab_name):
        joined_tabs = self.db_controller.get_channels()

        title = '. . . Tab Not Found . . .'
        tab_content = {}

        for channel in joined_tabs:
            # if it is the right tab, add the channel
            # check tab_order or tab_name
            try:
                if (isinstance(tab_order_or_tab_name, int) and channel.Tab.order == tab_order_or_tab_name) \
                        or (channel.Tab.name.replace('-', ' ').replace('_', ' ').lower() == tab_order_or_tab_name.replace('-', ' ').replace('_', ' ').lower()):
                    # gather info
                    row_order = channel.Row.order
                    format = channel.ColumnFormat.format
                    column_number = channel.Column.column_num
                    column_order = channel.Column.order
                    channel_model = channel.Channel

                    # create the array structure as needed
                    if row_order not in tab_content:
                        tab_content[row_order] = {
                            'format': format,
                            'columns': {}
                        }
                    if column_number not in tab_content[row_order]['columns']:
                        tab_content[row_order]['columns'][column_number] = {}

                    tab_content[row_order]['columns'][column_number][column_order] = channel_model

                    title = channel.Tab.name
            except:
                continue

        return title, tab_content

    def get_tabs(self):
        tabs = self.db_controller.get_tabs()
        tab_names = []
        for tab in tabs:
            tab_names.append(tab.Tab.name)

        return tab_names
