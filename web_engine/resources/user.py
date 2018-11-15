import sqlite3
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

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query_insert = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query_insert, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": f"User '{data['username']}' is registered."}, 201
