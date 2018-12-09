from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    -H "Authorization: JWT eyJ0eX...6CYqIgC90MI" \
    localhost:5000/item/test

curl localhost:5000/item/piano \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"price":"15"}'

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
    -d '{"username": "Habib", "password": "Habib"}'
"""

# POST /auth
"""
curl \
    localhost:5000/auth \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"username": "ali", "password": "asdf"}'
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
