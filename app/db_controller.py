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

