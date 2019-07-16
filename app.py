import os

from flask import Flask, request, jsonify, _app_ctx_stack
from flask_restful import Api, Resource
from auth.auth import AuthError, requires_auth

from flask_cors import CORS


from resources.user_resource import UserRegister, UserList, User
from resources.love_note_resource import LoveNote, LoveNoteList


app = Flask(__name__)
CORS(app)

#DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') #DATABSE_URL defined in heroku, locally use sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.environ.get('SECRET_KEY')


api = Api(app)




@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response




api.add_resource(LoveNote, '/api/note/<int:id>')
api.add_resource(LoveNoteList, '/api/notes')
api.add_resource(User, '/api/user/<int:id>')
api.add_resource(UserList, '/api/users')
api.add_resource(UserRegister, '/api/register')

#TODO- something like this api.add_resource(Auth, '/api/users/auth')
#TODO - create auth model or adapt user model, update database columns
# JS example users.string('auth0_sub', 255)

if __name__ == '__main__':
    from db import db #imports at bottom of code, because of circular imports
    db.init_app(app)
    port = int(os.environ.get("PORT", 6000))
    app.run(debug=True, host='0.0.0.0', port=port)

