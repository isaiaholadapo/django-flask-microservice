from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dapz4dappy@localhost/microservice_main'
app.config['SECRET_KEY'] = 'aa59e9c8d9d'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass()
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/product/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://localhost:8000/api/user')
    jsoni = req.json()
    try:
        product_user = ProductUser(user_id=jsoni['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish('product_liked', id)
    except:
        abort(400, 'You have liked this product already')
    return jsonify({
        "message": "success"
    })

if __name__ == "__main__":
    app.run(debug=True)
