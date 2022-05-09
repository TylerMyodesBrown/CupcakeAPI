from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_wtforms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }


@app.route('/api/cupcakes', methods=['POST', 'GET'])
def cupcake_page():
    """Sends List of all Cupcakes"""
    if request.method == 'POST':
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image = request.json["image"]

        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

        serialized = serialize_cupcake(new_cupcake)
        return ( jsonify(cupcake=serialized), 201 )

    else:
        cupcakes = Cupcake.query.all()
        serialized = [serialize_cupcake(c) for c in cupcakes]

        return jsonify(cupcakes=serialized)
    

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET', 'PATCH', 'DELETE'])
def cupcake_details(cupcake_id):
    if request.method == 'DELETE':
        '''Delete Cupcake'''
        Cupcake.query.filter_by(id=cupcake_id).delete()
        db.session.commit()
        return (jsonify({'message': "Deleted"}), 201)
        
    elif request.method == 'PATCH':
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image = request.json["image"]

        cake = Cupcake.query.filter_by(id=cupcake_id).first()
    
        cake.flavor = flavor
        cake.size = size
        cake.rating = rating
        cake.image = image
    
        db.session.add(cake)
        db.session.commit()
        serialized = serialize_cupcake(cupcake)
        return ( jsonify(cupcake=serialized), 201 )
    else:
        cupcake = Cupcake.query.get(cupcake_id)
        serialized = serialize_cupcake(cupcake)

        return jsonify(cupcake=serialized)