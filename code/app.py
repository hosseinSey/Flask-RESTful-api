from flask import Flask, request
import sys
sys.path.append('/Users/hosseins/Developer/programming_practice/flask_app/venv/lib/python3.6/site-packages')
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)

app.secret_key = "a_secret"
jwt = JWT(app, authenticate, identity)  # /auth
"""
curl localhost:5000/auth \
   -H "Content-Type: application/json" \
   -d '{"username":"hossein", "password":"pass"}'
"""

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field can not be left blank!"
    )

    @jwt_required()
    def get(self, name):
        """
        Test:
        curl localhost:5000/item/piano \
            -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDA3NzQ0MjEsImlhdCI6MTU0MDc3NDEyMSwibmJmIjoxNTQwNzc0MTIxLCJpZGVudGl0eSI6MX0.eDXrAsljEgHw912gsD_eFXTxbB2SNYAAjtoRWhTQMcc"
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

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = {
            "name": name,
            "price": data.get("price")
        }
        items.append(item)
        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {
                "name": name,
                "price": data['price']
            }
            items.append(item)

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": f"Item {name} deleted."}


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(debug=True)
