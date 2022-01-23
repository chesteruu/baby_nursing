from datetime import timezone, datetime

from models.poo import Poo
from models.nursing import Nursing
from models.bath import Bath

from sqlalchemy import func

from website import db


def _get_last_poo_time():
    last_poo_time: datetime = db.session.query(func.max(Poo.poo_time)).scalar()
    return last_poo_time.replace(tzinfo=timezone.utc).astimezone() if last_poo_time else datetime.min


def _get_last_nursing_time():
    last_nursing_time = db.session.query(func.max(Nursing.feeding_time)).scalar()
    return last_nursing_time.replace(tzinfo=timezone.utc).astimezone() if last_nursing_time else datetime.min


def _get_last_bath_time():
    last_bath_time = db.session.query(func.max(Bath.bath_time)).scalar()
    return last_bath_time.replace(tzinfo=timezone.utc).astimezone() if last_bath_time else datetime.min


class NursingProcessor:
    def __init__(self):
        self._last_poo_time = _get_last_poo_time()
        self._last_nursing_time = _get_last_nursing_time()
        self._last_bath_time = _get_last_bath_time()

    def add_poo(self, poo_time=None, is_sick = False):
        poo = Poo()
        poo.poo_time = poo_time if poo_time else datetime.utcnow()
        poo.is_sick = is_sick
        db.session.add(poo)
        db.session.commit()

        self._last_poo_time = poo_time

    def add_nursing(self, breast_feeding_ml=0, milk_feeding_ml=0, feed_time=None):
        if not breast_feeding_ml and not milk_feeding_ml:
            raise ValueError("At least feed something")

        nursing = Nursing()
        nursing.feeding_time = feed_time if feed_time else datetime.utcnow()
        nursing.breast_feeding_ml = breast_feeding_ml
        nursing.milk_feeding_ml = milk_feeding_ml

        db.session.add(nursing)
        db.session.commit()

        self._last_nursing_time = feed_time

    def get_last_poo_time(self):
        self._last_poo_time = _get_last_poo_time()
        return self._last_poo_time

    def get_last_nursing_time(self):
        self._last_nursing_time = _get_last_nursing_time()
        return self._last_nursing_time

    def get_all_nursing(self):
        return Nursing.query.order_by(Nursing.id.desc()).all()

    def get_nursing_by_id(self, filter_id: int):
        return Nursing.query.filter_by(id = filter_id).first()

    def update_nursing(self, nursing: Nursing):
        nursingdb = Nursing.query.filter_by(id = nursing.id).first()
        if nursingdb is None:
            raise FileNotFoundError("Record not found {}".format(id))
        nursingdb.feeding_time = nursing.feeding_time
        nursingdb.milk_feeding_ml = nursing.milk_feeding_ml

        db.session.commit()

    def delete_nursing(self, _id: int):
        Nursing.query.filter_by(id=_id).delete()
        db.session.commit()

    def get_all_poo(self):
        return Poo.query.order_by(Poo.id.desc()).all()

    def add_bath(self, bath_time=None):
        bath = Bath()
        bath.bath_time = bath_time if bath_time else datetime.utcnow()
        db.session.add(bath)
        db.session.commit()

        self._last_bath_time = bath.bath_time

    def get_last_bath_time(self):
        self._last_bath_time = _get_last_bath_time()
        return self._last_bath_time


