from flask import session
from flask import current_app

from app import app


class DashboardController(object):

    def __init__(self):
        pass


    def before_request(self):
        print "BEFORE REQUEST"

    def init_user():

        dev = current_app.config['ENVIRON'] != 'prod'

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

        if 'top_nav' not in session.keys():
            get_nav()

        if 'user_email' not in session.keys() and session['username']:
            # todo, get prefered email (alias) from wsapi once its added.
            session['user_email'] = session['username'] + "@bethel.edu"

        if 'name' not in session.keys() and session['username']:
            get_users_name()

    def get_user():
        if current_app.config['ENVIRON'] == 'prod':
            username = request.environ.get('REMOTE_USER')
        else:
            username = current_app.config['TEST_USER']

        session['username'] = username

    def get_users_name(username=None):
        if not username:
            username = session['username']
        url = current_app.config['API_URL'] + "/username/%s/names" % username
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
        url = current_app.config['API_URL'] + "/username/%s/roles" % username
        r = requests.get(url, auth=(current_app.config['API_USERNAME'], current_app.config['API_PASSWORD']))
        roles = fjson.loads(r.content)
        ret = []
        for key in roles.keys():
            ret.append(roles[key]['userRole'])

        session['roles'] = ret

        return ret

    def get_nav():
        html = render_template('nav.html', **locals())
        session['top_nav'] = html

    if '/public/' not in request.path and '/api/' not in request.path:
        init_user()
        get_nav()
    else:
        session['username'] = 'tinker'
        session['groups'] = []
        session['roles'] = []