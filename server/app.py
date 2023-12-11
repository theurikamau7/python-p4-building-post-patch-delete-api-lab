#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'GET':
        bakeries = Bakery.query.all()
        bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

        response = make_response(
            jsonify(bakeries_serialized),
            200
        )
        return response
    elif request.method == 'POST':
        name = request.form.get('name')
        new_bakery = Bakery(name=name)
        db.session.add(new_bakery)
        db.session.commit()

        response = make_response(
            jsonify(new_bakery.to_dict()),
            201
        )
        return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return jsonify({'error': 'Bakery not found'}), 404

    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        return response
    elif request.method == 'PATCH':
        name = request.form.get('name')
        if name:
            bakery.name = name
        db.session.commit()

        response = make_response(
            jsonify(bakery.to_dict()),
            200
        )
        return response
    elif request.method == 'DELETE':
        db.session.delete(bakery)
        db.session.commit()

        response = make_response(
            jsonify({'message': 'Bakery deleted'}),
            200
        )
        return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()

    response = make_response(
        jsonify(new_baked_good.to_dict()),
        201
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return jsonify({'error': 'Baked Good not found'}), 404

    db.session.delete(baked_good)
    db.session.commit()

    response = make_response(
        jsonify({'message': 'Baked Good deleted'}),
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)