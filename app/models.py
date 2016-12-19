from app import app, db


class User(db.Model):
    __tablename__ = 'dashboard_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username


class Role(db.Model):
    __tablename__ = 'dashboard_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name


class UserRole(db.Model):
    __tablename__ = 'dashboard_userrole'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('dashboard_role.id'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id


class Tab(db.Model):
    __tablename__ = 'dashboard_tab'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_user.id'))
    name = db.Column(db.String(20), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, name, order):
        self.user_id = user_id
        self.name = name
        if order < 0:
            raise ValueError('order must be greater than or equal to 0')
        self.order = order


class Row(db.Model):
    __tablename__ = 'dashboard_row'

    id = db.Column(db.Integer, primary_key=True)
    tab_id = db.Column(db.Integer, db.ForeignKey('dashboard_tab.id'))
    order = db.Column(db.Integer, nullable=False)
    column_format = db.Column(db.Integer, db.ForeignKey('dashboard_column_format.id'))

    def __init__(self, tab_id, order, column_format):
        self.tab_id = tab_id
        if order < 0:
            raise ValueError('order must be greater than or equal to 0')
        self.order = order
        self.column_format = column_format


class ColumnFormat(db.Model):
    __tablename__ = 'dashboard_column_format'

    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String, nullable=False)

    def __init__(self, format):
        self.format = format


class Column(db.Model):
    __tablename__ = 'dashboard_column'

    id = db.Column(db.Integer, primary_key=True)
    row_id = db.Column(db.Integer, db.ForeignKey('dashboard_row.id'))
    column_num = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('dashboard_channel.id'), nullable=False)

    def __init__(self, row_id, column_num, order, channel_id):
        self.row_id = row_id
        if column_num not in [0, 1, 2, 3]:
            raise ValueError('column_num must be 0, 1, 2, or 3')
        self.column_num = column_num
        if order < 0:
            raise ValueError('order must be greater than or equal to 0')
        self.order = order
        # todo could put a check in the init to make sure this table exists, and the ID exists within that table
        self.channel_id = channel_id


class Channel(db.Model):
    __tablename__ = 'dashboard_channel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    channel_class_name = db.Column(db.String(40))
    min_size = db.Column(db.Integer, nullable=False) # todo between 1 and 12 or has to be 6 or 12?

    def __init__(self, name, channel_class_name, min_size):
        self.name = name
        self.channel_class_name = channel_class_name
        if min_size < 3:
            raise ValueError("min_size must be at least 3, otherwise the columns don't work well")
        self.min_size = min_size


class Log(db.Model):
    __tablename__ = 'dashboard_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_user.id'))
    activity = db.Column(db.String(120), nullable=False)
    data = db.Column(db.PickleType) #  no idea what to do here. this sounded interesting though.
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, activity, data, date):
        self.user_id = user_id
        self.activity = activity
        self.data = data
        self.date = date
