

from db.user import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SuccessMessageSchema, UserSchema, UserQuerySchema


blp = Blueprint("Users", __name__, description="Operations on users")


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
        password = request_data["password"]
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