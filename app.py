import os

from flask import Flask, request, jsonify, _app_ctx_stack
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate

from db import db

from resources.user_resource import UserRegister, UserList, User
from resources.love_note_resource import LoveNote, LoveNoteList
from auth.auth import AuthError



app = Flask(__name__)


#DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get('SECRET_KEY')


CORS(app)
api = Api(app)
migrate = Migrate(app, db)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


api.add_resource(LoveNote, '/api/note/<int:id>','/api/note/create')
api.add_resource(LoveNoteList, '/api/notes/<int:user_id>')
api.add_resource(User, '/api/user/<int:id>','/api/user/delete/<int:id>')
api.add_resource(UserList, '/api/users')
api.add_resource(UserRegister, '/api/register')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=6000, debug=True)

