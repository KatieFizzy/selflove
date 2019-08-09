from flask_restful import Resource, reqparse
from models.user_model import UserModel
from auth.auth import requires_auth


class UserRegister(Resource):

    method_decorators = [requires_auth]

    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        #required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phone',
                        type=str,
                        #required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        #required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('send_frequency',
                        type=str,
                        help="This field cannot be blank."
                        )
    parser.add_argument('send_method',
                        type=str,
                        help="This field cannot be blank."
                        )
    parser.add_argument('sending_status',
                        type=bool,
                        help="This field expects True or False"
                        )

    parser.add_argument('sub',
                         location='headers'
                        )

    #TODO - add put method

    def get(self):
        print("-- starting -- GET() VERIFY USER___________________________________")
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_sub(data['sub'])

        if user:
            return (False)
            #FE behavior - sets redux store's signUpUser to false if user exists
        return (True)
        #FE behavior - sets redux store's signUpUser to true if user does not exist




    def post(self):
        print("-- starting -- POST() CREATE USER___________________________________")
        data = UserRegister.parser.parse_args()
        print("-- USER DATA (create) ___________________________________", data,
              "________________________________")

        if UserModel.find_by_sub(data['sub']):
            return {"message": "A user with that auth already exists"}, 400

        user = UserModel(**data)
        print("USER OBJECT (create) ___________________________________", user,
              "________________________________")

        user.save_to_db()

        return user.json(), 201


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

class User(Resource):
    print("-- starting -- GET() FETCH USER___________________________________")
    def get(self, id):
        user = UserModel.find_by_id(id)
        print("USER OBJECT (fetch) ___________________________________", user,
              "________________________________")

        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, id):
        print("-- starting --DELETE() DELETE USER___________________________________")
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted.'}
        return {'message': 'user not found.'}, 404

