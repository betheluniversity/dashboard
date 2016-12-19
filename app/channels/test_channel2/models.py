from app import app, db

class TestChannel2Model(db.Model):
    __tablename__ = 'dashboard_test_channel'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_user.id'))
    color = db.Column(db.String(80), nullable=False, default='red')

    def __init__(self, user_id, color):
        self.user_id = user_id
        self.color = color
