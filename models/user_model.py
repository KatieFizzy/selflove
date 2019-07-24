from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    phone = db.Column(db.String(12))
    email = db.Column(db.String)
    sub = db.Column(db.String)
    send_frequency = db.Column(db.String)
    send_method = db.Column(db.String)
    sending_status = db.Column(db.Boolean)

    love_notes = db.relationship('LoveNoteModel', lazy='dynamic')



    def __init__(self, username,phone,email,sub, send_frequency=None, send_method=None,sending_status=False):
        self.username = username
        self.phone = phone
        self.email = email
        self.sub  = sub
        self.send_frequency = send_frequency
        self.send_method = send_method
        self.sending_status = sending_status

    def json(self):
        return {'username': self.username,
                'id': self.id,
                'email':self.email,
                'phone':self.phone,
                'send_frequency': self.send_frequency,
                'send_method': self.send_method,
                'sending_status': self.sending_status,
                'love_notes': [love_note.json() for love_note in self.love_notes.all()]
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_sub(cls, sub):
        return cls.query.filter_by(sub=sub).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
