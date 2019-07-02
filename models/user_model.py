from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    phone = db.Column(db.String(12))
    email = db.Column(db.String)

    love_notes = db.relationship('LoveNoteModel', lazy='dynamic')

    '''   NOTES to self:
          the above is a back-reference, opposite of foreign key 
          it allows user to see which notes in the notes table it owns 

          '''

    def __init__(self, username, password,phone,email):
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email

    def json(self):
        return {'username': self.username, 'id': self.id, 'love_notes': [love_note.json() for love_note in self.love_notes.all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()#TODO rewatch explanation

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()#TODO rewatch explanation

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
