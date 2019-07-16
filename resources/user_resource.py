from flask_restful import Resource, reqparse
from models.user_model import UserModel
from .auth import requires_auth


class UserRegister(Resource):

    method_decorators = [requires_auth]

    parser = reqparse.RequestParser() #can also use with form payloads

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('profile.sub',
                         location='headers'
                        )


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_auth0_sub(data['auth0_sub']):
            return {"message": "A user with that auth already exists"}, 400

        user = UserModel(data['username'], data['password'], data['phone'], data['email'], data['auth0_sub'] )
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

class User(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404