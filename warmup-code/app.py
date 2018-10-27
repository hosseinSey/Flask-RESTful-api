from flask import Flask, jsonify, request
from time import sleep

app = Flask(__name__)

stores = [
    {
        'name': "My First Store",
        'items': [
            {
                'name': 'lamp',
                'price': '12.5',
            },
            {
                'name': 'desk',
                'price': '34',
            }
        ]
    },
    {
        'name': "simple",
        'items': [
        ]
    },
]


@app.route('/')
def home():
    return "Hello world"


@app.route('/stores', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data.get('name'),
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>/item', methods=['POST'])
def add_item(name):
    request_data = request.get_json()
    # pdb.set_trace()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data.get('name'),
                'price': request_data.get('price')
            }
            store['items'].append(new_item)
            return jsonify(store["items"])
    return "500"


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify(store['items'])
    return f'{name} not found'


@app.route('/ping')
def ping():
    sleep(0.1)
    return "pong"


app.run(port=5000, debug=True)
