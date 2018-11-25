import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"'{name}' already exits!"}, 400

        # data = request.get_json()
        data = self.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.insert()
        except Exception:
            return {"message": "An error occurred during item insertion."}, 500
        return item.json(), 201

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])
        if item is None:
            try:
                updated_item.insert(updated_item)
            except Exception:
                return {"message": "An error occured!"}, 500
        else:
            try:
                updated_item.update()
            except Exception:
                return {"message": "An error occured!"}, 500
        return {"message": f"Item {name} updated."}, 200

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message": f"Item {name} deleted."}


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        results = list(cursor.execute(query))
        items = []
        for r in results:
            items.append({"name": r[0], "price": r[1]})
        connection.close()
        return {"items": items}
