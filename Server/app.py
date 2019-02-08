from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import datetime

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init Ma
ma = Marshmallow(app)


# Product Class/Model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    state = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    int_temp = db.Column(db.Float)
    ext_temp = db.Column(db.Float)
    cool_temp = db.Column(db.Float)
    voltage = db.Column(db.Float)
    check_in = db.Column(db.String(200))

    def __init__(self, name, state, status, int_temp, ext_temp, cool_temp, voltage, check_in):
        self.name = name
        self.state = state
        self.status = status
        self.int_temp = int_temp
        self.ext_temp = ext_temp
        self.cool_temp = cool_temp
        self.voltage = voltage
        self.check_in = check_in


# Car Schema
class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'state', 'status', 'int_temp', 'ext_temp', 'cool_temp', 'voltage', 'check_in')


# Init Schema
car_schema = CarSchema(strict=True)


@app.route('/car/<id>', methods=['POST'])
def add_product(id):
    car = Car.query.get(id)

    status = request.json['status']
    int_temp = request.json['int_temp']
    ext_temp = request.json['ext_temp']
    cool_temp = request.json['cool_temp']
    voltage = request.json['voltage']
    check_in = datetime.datetime.now()

    if not car:
        state = False
        car = Car('Car', state, status, int_temp, ext_temp, cool_temp, voltage, check_in)
        db.session.add(car)
        db.session.commit()
        print('Create Car', car)
    else:
        print('Update Car', car)
        car.status = status
        car.int_temp = int_temp
        car.ext_temp = ext_temp
        car.cool_temp = cool_temp
        car.voltage = voltage
        car.check_in = check_in
        db.session.commit()

    return jsonify(car.state)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
