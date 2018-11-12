from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, Items

app = Flask(__name__)
api = Api(app)

app.secret_key = "a_secret"
jwt = JWT(app, authenticate, identity)  # /auth
"""
curl localhost:5000/auth \
   -H "Content-Type: application/json" \
   -d '{"username":"hossein", "password":"pass"}'
"""


@app.route('/ping')
def ping():
    return "pong\n"


api.add_resource(Item, '/item/<string:name>')
"""
curl \
    -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE5NzI2ODAsImlhdCI6MTU0MTk3MjM4MCwibmJmIjoxNTQxOTcyMzgwLCJpZGVudGl0eSI6MX0.928O_sNvWQaO1WU7uxcqINkP_jb5oAlLUmaGvM5W-2M" \
    localhost:5000/item/test

curl localhost:5000/item/book \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"price":"20"}'

curl localhost:5000/item/book \
    -X PUT \
    -H "Content-Type: application/json" \
    -d '{"price":"12.3"}'
"""


api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
"""
curl \
    localhost:5000/register \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "Ali", "password": "qwerty"}'
"""

# POST /auth
"""
curl \
    localhost:5000/auth \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "Ali", "password": "qwerty"}'
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
