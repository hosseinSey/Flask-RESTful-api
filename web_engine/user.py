import sqlite3
from flask_restful import Resource, reqparse
from flask import request


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        find_user_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(find_user_query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        find_id_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(find_id_query, (id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


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
        if User.find_by_username(data['username']):
            return {"message": "User already exists"}, 400
            
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query_insert = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query_insert, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": f"User '{data['username']}' is registered."}, 201
