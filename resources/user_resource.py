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



    def validOptions(self):
        print(" -------- ValidOptions called ----------")
        data = UserRegister.parser.parse_args()
        # validating received an expected input from FE user preferences
        print(data)
        sendFrequencyOptions = ['daily', 'weekly', '2X/week', 'monthly', '2X/month', 'null']
        sendMethodOptions = ['email', 'phone', 'null']
        sendingStatusOptions = [True, False, 'null']


        if data['send_frequency'] in sendFrequencyOptions:
            print("first if")
            if data['send_method'] in sendMethodOptions:
                print("second if")
                if data['sending_status'] in sendingStatusOptions:
                    print("third if")
                    validOptions = True
                    print("validOptions = -",validOptions)
                    return validOptions

    def get(self):

        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_sub(data['sub'])
        print("GET",data)

        if user:
            return user.json()
        return (True)
        #FE behavior - sets redux store's signUpUser to true if user does not exist

    def post(self):
        data = UserRegister.parser.parse_args()
        print("UserRegister POST",data)

        if UserModel.find_by_sub(data['sub']):
            return {"message": "A user with that auth already exists"}, 400

        #if user preference inputs are valid, create user
        if UserRegister.validOptions(self):
            print(" ---- ValidOptions return value in post ----")
            user = UserModel(**data)
            user.save_to_db()
            return user.json(), 201



class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

class User(Resource):

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

    def validOptions(self):
        print(" -------- ValidOptions called ----------")
        data = UserRegister.parser.parse_args()
        # validating received an expected input from FE user preferences
        print(data)
        sendFrequencyOptions = ['daily', 'weekly', '2X/week', 'monthly', '2X/month', 'null']
        sendMethodOptions = ['email', 'phone', 'null']
        sendingStatusOptions = [True, False, 'null']

        if data['send_frequency'] in sendFrequencyOptions:
            print("first if")
            if data['send_method'] in sendMethodOptions:
                print("second if")
                if data['sending_status'] in sendingStatusOptions:
                    print("third if")
                    validOptions = True
                    print("validOptions = -", validOptions)
                    return validOptions

    def get(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_sub(data['sub'])

        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def post(self):
        data = User.parser.parse_args()

        if UserModel.find_by_sub(data['sub']):
            return {"message": "A user with that auth already exists"}, 400

        # if user preference inputs are valid, create user
        if User.validOptions(self):
            print(" ---- ValidOptions return value in post ----")
            user = UserModel(**data)
            user.save_to_db()
            return user.json(), 201

    def put(self, id):
        data = User.parser.parse_args()
        user = UserModel.find_by_id(id)

        if user:
            if User.validOptions(self):
                user.username= data['username']
                user.email = data['email']
                user.phone = data['phone']
                user.send_frequency = data['send_frequency']
                user.send_method = data['send_method']
                user.sending_status = data['sending_status']

        user.save_to_db()
        return user.json(), 201


    def delete(self, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted.'}
        return {'message': 'user not found.'}, 404

