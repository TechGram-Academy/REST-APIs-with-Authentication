

from db.user import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SuccessMessageSchema, UserSchema, UserQuerySchema
import hashlib
from flask_jwt_extended import create_access_token


blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/login")
class Login(MethodView):

    def __init__(self):
        self.db = UserDatabase()
   
    @blp.arguments(UserSchema)
    def post(self, request_data):
    
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        
        result = self.db.verify_user(username, password)
        if result:
            return create_access_token(identity="indrajeet")
        abort(400, message="Username or password is incorrect")

@blp.route("/user")
class User(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def get(self, args):
        id = args.get('id') 
        result = self.db.get_user(id)
        if result is None:
            abort(404, message="User doesn't exist")
        return result

   

    @blp.arguments(UserSchema)
    @blp.response(200, SuccessMessageSchema)
    def post(self, request_data):
        # check if already exists
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()

        if self.db.add_user(username, password):
            return {"message": "User added succesfully"}, 201
        return abort(403, message="User already exists")

    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')
        if self.db.delete_user(id):
            return {'message': 'User deleted'}   
        abort(404, message="Given user id doesn't exist.")
