import os

from flask import Flask, request, jsonify, _request_ctx_stack
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import cross_origin

from security import authenticate, identity

from resources.user_resource import UserRegister, UserList, User
from resources.love_note_resource import LoveNote, LoveNoteList


AUTH0_DOMAIN = 'dev-hoj9hf7z.auth0.com'
API_AUDIENCE = YOUR_API_AUDIENCE
ALGORITHMS = ["RS256"]

APP = Flask(__name__)

# AuthO Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated



APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') #DATABSE_URL defined in heroku, locally use sqlite
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['PROPAGATE_EXCEPTIONS'] = True
#APP.secret_key = 'something' #TODO UPDATE ME
api = Api(APP)


#@app.before_first_request
#def create_tables():
    #db.create_all()


#jwt = JWT(app, authenticate, identity)  # /auth
#authenticate is a function, the returned user becomes identity


api.add_resource(LoveNote, 'api/note/<int:id>')
api.add_resource(LoveNoteList, 'api/notes')
api.add_resource(UserRegister, 'api/register')
api.add_resource(User, 'api/user/<int:id>')
api.add_resource(UserList, 'api/users')



if __name__ == '__main__':
    from db import db #imports at bottom of code, because of circular imports
    db.init_app(APP)
    #app.run(port=port, debug=True)
    port = int(os.environ.get("PORT", 6000))
    APP.run(debug=True, host='0.0.0.0', port=port)

