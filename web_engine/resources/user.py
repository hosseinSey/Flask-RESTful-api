from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username',
            type=str,
            required=True,
            help="This field can not be blank"
        )
        self.parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This filed can not be blank"
        )

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400
        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": f"User '{data['username']}' is registered."}, 201
