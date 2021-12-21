from datetime import timezone, datetime

from models.poo import Poo
from models.nursing import Nursing

from sqlalchemy import func

from website import db


def _get_last_poo_time():
    last_poo_time: datetime = db.session.query(func.max(Poo.poo_time)).scalar()
    return last_poo_time.replace(tzinfo=timezone.utc).astimezone(tz=None) if last_poo_time else datetime.min


def _get_last_nursing_time():
    last_nursing_time = db.session.query(func.max(Nursing.feeding_time)).scalar()
    return last_nursing_time.replace(tzinfo=timezone.utc).astimezone(tz=None) if last_nursing_time else datetime.min


class NursingProcessor:
    def __init__(self):
        self._last_poo_time = _get_last_poo_time()
        self._last_nursing_time = _get_last_nursing_time()

    def add_poo(self, poo_time=None):
        poo = Poo()
        poo.poo_time = poo_time if poo_time else datetime.utcnow()
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

