from db import db
from sqlalchemy.sql import func
import datetime

class LoveNoteModel(db.Model):
    __tablename__ = 'love_notes'

    id = db.Column(db.Integer, primary_key=True)
    body =  db.Column(db.String(300))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, body, user_id = None):
        self.body = body
        self.user_id = user_id


    def json(self):
        return {'id': self.id, 'user_id':self.user_id, 'time_created':str(self.time_created), 'body': self.body}


    @classmethod
    def find_by_body(cls, body, user_id):
        return cls.query.filter_by(body=body, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()