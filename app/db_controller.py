from app.models import *
from app import db
from flask import session


class DBController(object):
    def __init__(self):
        self.db_session = db.session

    def get_current_users_id(self):
        user = self.db_session.query(User).filter(User.username == session['username']).first()

        return user.id

    def get_channels(self):
        channels = self.db_session.query(User, Tab, Row, ColumnFormat, Column, Channel)\
            .join(Tab)\
            .join(Row)\
            .join(ColumnFormat)\
            .join(Column)\
            .join(Channel)\
            .filter(User.username==session['username'])\
            .order_by(Tab.order)\
            .order_by(Row.order)\
            .order_by(Column.column_num)\
            .order_by(Column.order)\
            .all()

        return channels

    def get_all_channels_values(self):
        results = self.db_session.query(Channel).order_by(Channel.name).all()
        channels = []
        for result in results:
            channels.append(result.name)

        return channels

    def get_column_formats_values(self):
        results = self.db_session.query(ColumnFormat).order_by(ColumnFormat.order).all()
        formats = []
        for result in results:
            formats.append(result.format)

        return formats

    def get_tabs(self):
        tabs = self.db_session.query(User, Tab)\
            .join(Tab)\
            .filter(User.username==session['username'])\
            .order_by(Tab.order)\
            .all()

        return tabs

    def clear_db_generated_content(self):
        User.query.delete()
        UserRole.query.delete()
        Tab.query.delete()
        Row.query.delete()
        Column.query.delete()

        return True

    def create_new_user(self):
        user = User.query.filter(User.username == session['username']).first()

        # if user does not exist, then . . .
        if user is None:

            # create user
            new_user = User(username=session['username'])
            self.db_session.add(new_user)
            self.db_session.commit() # commit, in order to get autogenerated id's

            # create roles
            new_user_role = UserRole(user_id=new_user.id, role_id=2)
            self.db_session.add(new_user_role)

            # create tab1
            new_tab1 = Tab(user_id=new_user.id, name='Home', order=1)
            self.db_session.add(new_tab1)
            self.db_session.commit()

            # create row1
            row1 = Row(new_tab1.id, 1, 1)
            self.db_session.add(row1)
            self.db_session.commit()

            # create row1 cols
            new_column = Column(row1.id, 0, 0, 2)
            self.db_session.add(new_column)

            new_column = Column(row1.id, 0, 1, 2)
            self.db_session.add(new_column)

            new_column = Column(row1.id, 0, 2, 2)
            self.db_session.add(new_column)

            new_column = Column(row1.id, 1, 0, 2)
            self.db_session.add(new_column)

            new_column = Column(row1.id, 1, 1, 2)
            self.db_session.add(new_column)

            # create row2
            row2 = Row(new_tab1.id, 2, 2)
            self.db_session.add(row2)
            self.db_session.commit()

            # create row2 cols
            new_column = Column(row2.id, 0, 0, 1)
            self.db_session.add(new_column)

            new_column = Column(row2.id, 1, 0, 1)
            self.db_session.add(new_column)

            new_column = Column(row2.id, 2, 0, 1)
            self.db_session.add(new_column)

            # create tab2
            new_tab2 = Tab(user_id=new_user.id, name='Another Tab', order=2)
            self.db_session.add(new_tab2)
            self.db_session.commit()

            # create row3
            row3 = Row(new_tab2.id, 3, 3)
            self.db_session.add(row3)
            self.db_session.commit()

            # create row3 cols
            new_column = Column(row3.id, 0, 0, 3)
            self.db_session.add(new_column)

            self.db_session.commit()
            return True

        else:
            # user exists, so exit
            return False

    def init_db(self):
        # Todo: make this check more accurate? Maybe check if things exist individually
        if Role.query.filter(Role.name=='ROLE_ADMIN').first() is None:
            new_role = Role(name='ROLE_ADMIN')
            self.db_session.add(new_role)
            new_role = Role(name='ROLE_VIEWER')
            self.db_session.add(new_role)

            # create column_formats
            column_format1 = ColumnFormat('6-6',2)
            self.db_session.add(column_format1)
            column_format2 = ColumnFormat('4-4-4', 1)
            self.db_session.add(column_format2)
            column_format3 = ColumnFormat('12', 3)
            self.db_session.add(column_format3)

            new_channel = Channel('My Test Channel (minsize4)', 'TestChannel', 4)
            self.db_session.add(new_channel)
            new_channel = Channel('My Test Channel (minsize6)', 'TestChannel', 6)
            self.db_session.add(new_channel)
            new_channel = Channel('My Test Channel (minsize12)', 'TestChannel2', 12)
            self.db_session.add(new_channel)

            self.db_session.commit()
            return True
        else:
            return False
