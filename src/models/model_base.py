from src import db


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def commit(cls):
        db.session.commit()
