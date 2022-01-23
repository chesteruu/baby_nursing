from website import db


class Bath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bath_time = db.Column(db.DateTime)
