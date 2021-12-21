from website import db


class Nursing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breast_feeding_ml = db.Column(db.Integer())
    milk_feeding_ml = db.Column(db.Integer())
    feeding_time = db.Column(db.DateTime())

