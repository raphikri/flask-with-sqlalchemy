from flask import Flask, request, abort, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

BASE_URL = '/api/v1'


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (Order is important here!)
db = SQLAlchemy(app)
ma = Marshmallow(app)
from models import Product
from schemas import many_product_schema, one_product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()

    return render_template('home.html', products=products)

@app.route('/<int:product_id>')
def product_html(product_id):
    product = db.session.query(Product).get(product_id)
    return render_template('product.html', product=product)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['GET'])
def get_one_product(product_id):
    product = db.session.query(Product).get(product_id) # SQLAlchemy request => 'SELECT * FROM products where id = {product_id}'
    return one_product_schema.jsonify(product), 200

@app.route(f'{BASE_URL}/products', methods=['POST'])
def add_product():
    new_product = Product()
    new_product.name = request.get_json()["name"]
    new_product.description = request.get_json()["description"]
    #import pdb;pdb.set_trace()
    #for key, value in request.get_json().items():
    #    if value != None:
    #        new_product.key = value
    db.session.add(new_product)
    db.session.commit()
    return '', 201

@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = db.session.query(Product).get(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
