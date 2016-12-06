from app.models import *
from app import db
from flask import session


class DBController(object):
    def __init__(self):
        self.db_session = db.session

    def get_tabs_for_user(self, username):
        pass

    def get_joined_tabs(self):
        joined_tables = self.db_session.query(User, Tab, Row, Column, Channel)\
            .join(Tab)\
            .join(Row)\
            .join(Column)\
            .join(Channel)\
            .filter(User.username==session['username'])\
            .order_by(Tab.order)\
            .order_by(Row.order)\
            .order_by(Column.column_num)\
            .order_by(Column.order)\
            .all()

        return joined_tables

    def clear_db_generated_content(self):
        User.query().delete()
        UserRole.query().delete()
        Tab.query().delete()
        Row.query().delete()
        Column.query().delete()

        return True

    def create_new_user(self):
        user = User.query.filter(User.username == session['username']).first()

        # if user does not exist, then . . .
        if user is None:

            # create user
            new_user = User(username=session['username'])
            self.db_session.add(new_user)
            new_user = User.query.filter(User.username == session['username']).first()

            # create roles
            new_user_role = UserRole(user_id=new_user.id, role_id=2)
            self.db_session.add(new_user_role)

            # create tab
            new_tab = Tab(user_id=new_user.id, name='First Tab', order=1)
            self.db_session.add(new_tab)
            new_tab = Tab.query.filter(Tab.user_id == new_user.id).first()

            # create row
            new_row = Row(new_tab.id, 0)
            self.db_session.add(new_row)
            new_row = Row.query.filter(Row.id == new_tab.id).first()

            # create cols
            new_column = Column(new_row.id, 0, 0, 'test-channel00', '1')
            self.db_session.add(new_column)

            new_column = Column(new_row.id, 0, 2, 'test-channel02', '1')
            self.db_session.add(new_column)

            new_column = Column(new_row.id, 0, 1, 'test-channel01', '1')
            self.db_session.add(new_column)

            new_column = Column(new_row.id, 1, 0, 'test-channel10', '1')
            self.db_session.add(new_column)

            new_column = Column(new_row.id, 1, 1, 'test-channel01', '1')
            self.db_session.add(new_column)

            # create row
            new_row = Row(new_tab.id, 1)
            self.db_session.add(new_row)
            new_row = Row.query.filter(Row.id == new_tab.id).first()

            # create cols
            new_column = Column(new_row.id, 0, 0, 'test-channel00', '1')
            self.db_session.add(new_column)

            new_column = Column(new_row.id, 1, 0, 'test-channel10', '1')
            self.db_session.add(new_column)

            self.db_session.commit()
            return True

        else:
            # user exists, so exit
            return False

    def init_db(self):
        new_role = Role(name='ROLE_ADMIN')
        self.db_session.add(new_role)
        new_role = Role(name='ROLE_VIEWER')
        self.db_session.add(new_role)

        new_channel = Channel('My Test Channel', 'tablename?', 'TestChannel', 6)
        self.db_session.add(new_channel)

        self.db_session.commit()
        return True
