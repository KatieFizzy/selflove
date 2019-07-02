from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user_resource import UserRegister, UserList, User
from resources.love_note_resource import LoveNote, LoveNoteList




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'something' #TODO UPDATE ME
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth
#authenticate is a function, the returned user becomes identity


api.add_resource(LoveNote, '/love_note/<string:title>')
api.add_resource(LoveNoteList, '/love_notes')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')



if __name__ == '__main__':
    from db import db #imports at bottom of code, because of circular imports
    db.init_app(app)
    app.run(port=5000, debug=True)

