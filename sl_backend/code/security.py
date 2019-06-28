from werkzeug.security import safe_str_cmp
from models.user_model import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        #safe_str_cmp - compares strings safely
        return user


def identity(payload): #payload is contents of jwt token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)