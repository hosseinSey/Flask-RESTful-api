from flask import Flask, request
import sys
sys.path.append('/Users/hosseins/Developer/programming_practice/flask_app/venv/lib/python3.6/site-packages')
from flask_restful import Api, Resource
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth
# curl localhost:5000/auth
#   -H "Content-Type: application/json"
#   -d '{"username":"bob", "password":"asdf"}'

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return item

    def post(self, name):
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
