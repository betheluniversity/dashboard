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

        init_user_session()
        print self.create_new_user()

    def create_new_user(self):
        db_session = db.session

        user = User.query.filter(User.username==session['username']).first()

        # if user does not exist, then . . .
        if user is None:

            # create user
            new_user = User(username=session['username'])
            db_session.add(new_user)
            new_user = User.query.filter(User.username==session['username']).first()

            # create roles
            new_user_role = UserRole(user_id=new_user.id, role_id=2)
            db_session.add(new_user_role)

            # create tab
            new_tab = Tab(user_id=new_user.id, name='First Tab', order=1)
            db_session.add(new_tab)
            new_tab = Tab.query.filter(Tab.user_id==new_user.id).first()

            # create row
            new_row = Row(new_tab.id, 0)
            db_session.add(new_row)
            new_row = Row.query.filter(Row.id==new_tab.id).first()

            # create cols
            new_column = Column(new_row.id, 0, 0, 'test-channel00', '1')
            db_session.add(new_column)

            new_column = Column(new_row.id, 0, 2, 'test-channel02', '1')
            db_session.add(new_column)

            new_column = Column(new_row.id, 0, 1, 'test-channel01', '1')
            db_session.add(new_column)

            new_column = Column(new_row.id, 1, 0, 'test-channel10', '1')
            db_session.add(new_column)

            new_column = Column(new_row.id, 1, 1, 'test-channel01', '1')
            db_session.add(new_column)

            # create row
            new_row = Row(new_tab.id, 1)
            db_session.add(new_row)
            new_row = Row.query.filter(Row.id == new_tab.id).first()

            # create cols
            new_column = Column(new_row.id, 0, 0, 'test-channel00', '1')
            db_session.add(new_column)

            new_column = Column(new_row.id, 1, 0, 'test-channel10', '1')
            db_session.add(new_column)

            db_session.commit()
            return True

        else:
            # user exists, so exit
            return False

    def render_tab(self, tab_order):
        joined_tabs = self.db_controller.get_joined_tabs()

        return_array = {}
        for channel in joined_tabs:
            # if it is the right tab, add the channel
            # Todo: maybe move this to be a part of the sql?
            if channel.Tab.order == tab_order:
                # gather info
                row_order = channel.Row.order
                column_number = channel.Column.column_num
                column_order = channel.Column.order
                channel = channel.Channel

                # create the array structure as needed
                if row_order not in return_array:
                    return_array[row_order] = {}
                if column_number not in return_array[row_order]:
                    return_array[row_order][column_number] = {}

                return_array[row_order][column_number][column_order] = channel

        return return_array
