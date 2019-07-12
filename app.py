import os
import urllib
from functools import wraps
from jose import jwt
from flask import Flask
from flask_restful import Api
#from flask_jwt import JWT
#from flask_cors import CORS


#from security import authenticate, identity

from resources.user_resource import UserRegister, UserList, User
from resources.love_note_resource import LoveNote, LoveNoteList


auth0_domain = os.environ.get('AUTH0_DOMAIN')
api_audience = os.environ.get('API_ID')


app = Flask(__name__)

# Format error response and append status code.
def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return handle_error({'code': 'authorization_header_missing',
                                'description':
                                    'Authorization header is expected'}, 401)

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return handle_error({'code': 'invalid_header',
                                'description':
                                    'Authorization header must start with'
                                    'Bearer'}, 401)
        elif len(parts) == 1:
            return handle_error({'code': 'invalid_header',
                                'description': 'Token not found'}, 401)
        elif len(parts) > 2:
            return handle_error({'code': 'invalid_header',
                                'description': 'Authorization header must be'
                                 'Bearer + \s + token'}, 401)

        token = parts[1]
        jsonurl = urllib.request.urlopen('https://'+auth0_domain+'/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=unverified_header['alg'],
                    audience=api_audience,
                    issuer='https://'+auth0_domain+'/'
                )
            except jwt.ExpiredSignatureError:
                return handle_error({'code': 'token_expired',
                                    'description': 'token is expired'}, 401)
            except jwt.JWTClaimsError:
                return handle_error({'code': 'invalid_claims',
                                    'description': 'incorrect claims, please check the audience and issuer'}, 401)
            except Exception:
                return handle_error({'code': 'invalid_header',
                                    'description': 'Unable to parse authentication'
                                    ' token.'}, 400)

            _app_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        return handle_error({'code': 'invalid_header',
                             'description': 'Unable to find appropriate key'}, 400)
    return decorated


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') #DATABSE_URL defined in heroku, locally use sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'something' #TODO UPDATE ME
api = Api(app)


#@app.before_first_request
#def create_tables():
    #db.create_all()


#jwt = JWT(app, authenticate, identity)  # /auth
#authenticate is a function, the returned user becomes identity
# Controllers API
@app.route("/ping")
@cross_origin(headers=['Content-Type', 'Authorization'])
def ping():
    return jsonify({"message": "All good. You don't need to be authenticated to call this"})


@app.route("api/secured/ping")
@cross_origin(headers=['Content-Type', 'Authorization'])
@cross_origin(headers=['Access-Control-Allow-Origin', '*'])
@requires_auth
def securedPing():
    return jsonify({"message": "All good. You only get this message if you're authenticated"})


api.add_resource(LoveNote, 'api/note/<int:id>')
api.add_resource(LoveNoteList, 'api/notes')
api.add_resource(UserRegister, 'api/register')
api.add_resource(User, 'api/user/<int:id>')
api.add_resource(UserList, 'api/users')



if __name__ == '__main__':
    from db import db #imports at bottom of code, because of circular imports
    db.init_app(app)
    #app.run(port=port, debug=True)
    port = int(os.environ.get("PORT", 6000))
    app.run(debug=True, host='0.0.0.0', port=port)

