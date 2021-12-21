from website import db


class Poo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_sick = db.Column(db.Boolean)
    poo_time = db.Column(db.DateTime)