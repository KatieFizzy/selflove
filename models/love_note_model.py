from db import db


class LoveNoteModel(db.Model):
    __tablename__ = 'love_notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    body =  db.Column(db.String(300))
    #date_created = db.Column(db.DateTime)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    '''
      NOTES to self: 
      a user has notes
      the foreign key here is saying, I belong to this user

    '''


    def __init__(self, title, body, user_id = None ):
        self.title = title
        self.body = body
        #self.date_created=date_created
        self.user_id = user_id



    def json(self):
        return {'id': self.id,'title': self.title, 'body': self.body}



    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()