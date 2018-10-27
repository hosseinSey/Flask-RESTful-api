from flask import Flask, request
import sys
sys.path.append('/Users/hosseins/Developer/programming_practice/flask_app/venv/lib/python3.6/site-packages')
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)

app.secret_key = "a_secret"
jwt = JWT(app, authenticate, identity)  # /auth
"""
curl localhost:5000/auth \
   -H "Content-Type: application/json" \
   -d '{"username":"bob", "password":"asdf"}'
"""

items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        """
        Test:
        curl localhost:5000/item/piano \
            -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDA2ODI4ODAsImlhdCI6MTU0MDY4MjU4MCwibmJmIjoxNTQwNjgyNTgwLCJpZGVudGl0eSI6MX0.xHvwsd6-Ct1cT7Sf_XtqVS8PEDJD8OhW4fJ2H4XfdxE"
        """
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item

    def post(self, name):
        """
        testing:
        curl localhost:5000/item/piano \
            -X POST \
            -H "Content-Type: application/json" \
            -d '{"price":"20"}' \
        """
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"'{name}' already exits!"}, 400
        data = request.get_json()
        item = {
            "name": name,
            "price": data.get("price")
        }
        items.append(item)
        return item, 201


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(debug=True)
