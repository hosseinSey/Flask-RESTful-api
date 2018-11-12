from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field can not be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()
        return row

    # @jwt_required()
    def get(self, name):
        row = self.find_by_name(name)
        if row:
            return {"items": {"name": row[0], "price": row[1]}}
        return {"message": "Item not found"}, 400

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item["price"]))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item["name"]))
        connection.commit()
        connection.close()

    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"'{name}' already exits!"}, 400

        # data = request.get_json()
        data = self.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except Exception:
            return {"message": "An error occurred during item insertion."}, 500
        return item, 201

    def put(self, name):
        data = self.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}
        if item:
            self.update(updated_item)
        else:
            self.insert(updated_item)
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
