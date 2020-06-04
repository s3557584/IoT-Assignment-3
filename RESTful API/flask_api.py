"""
Task A: RESTful API

Written by: Ching Loo(s3557584)

Main file of the API
"""
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from marshmallow import fields
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import hashlib, binascii, os

api = Blueprint("api", __name__)



# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

class Admin(db.Model):
    """
    User Class/Model
    """
    adminUsername = db.Column(db.String(100), primary_key=True)
    adminName = db.Column(db.String(100))
    adminPassword = db.Column(db.String(1111))
    
    def __init__(self, adminUsername, adminName, adminPassword):
        self.adminUsername = adminUsername
        self.adminName = adminName
        self.adminPassword = adminPassword

class User(db.Model):
    """
    User Class/Model
    """
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    password = db.Column(db.String(1111))
    imageName = db.Column(db.String(100))
    
    def __init__(self, username, firstname, surname, password, imageName):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.password = password
        self.imageName = imageName

class Vehicle(db.Model):
    """
    Vehicle Class/Model
    """
    vehicleID = db.Column(db.Integer, primary_key=True)
    vehicleBrand = db.Column(db.String(100))
    vehicleModel = db.Column(db.String(100))
    rentalStatus = db.Column(db.Boolean)
    colour = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    cost = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=True)
    user = db.relationship("User", backref="parents")

    def __init__(self, vehicleBrand, vehicleModel, rentalStatus, colour, seats, latitude, longitude, cost, userID):
        self.vehicleBrand = vehicleBrand
        self.vehicleModel = vehicleModel
        self.rentalStatus = rentalStatus
        self.colour = colour
        self.seats = seats
        self.latitude = latitude
        self.longitude = longitude
        self.cost = cost
        self.userID = userID

class Records(db.Model):
    recordsID = db.Column(db.Integer, primary_key=True)
    dateRented = db.Column(db.String(100))
    vehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.vehicleID'), nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=True)
    user = db.relationship("User", backref="userTable")
    vehicle = db.relationship("Vehicle", backref="vehicleTable")
    def __init__(self, dateRented, vehicleID, userID):
        self.dateRented = dateRented
        self.vehicleID = vehicleID
        self.userID = userID

class AdminSchema(ma.Schema):
    """
    Admin Schema
    """
    adminUsername = fields.String(required=True)
    adminName = fields.String(required=True)
    adminPassword = fields.String(required=True)

class UserSchema(ma.Schema):
    """
    User Schema
    """
    userID = fields.Integer()
    username = fields.String(required=True)
    firstname = fields.String(required=True)
    surname = fields.String(required=True)
    password = fields.String(required=True)
    imageName = fields.String(required=True)

class VehicleSchema(ma.Schema):
    """
    User Schema
    """
    vehicleID = fields.Integer()
    vehicleBrand = fields.String(required=True)
    vehicleModel = fields.String(required=True)
    rentalStatus = fields.String(required=True)
    colour = fields.String(required=True)
    seats = fields.Integer(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    cost = fields.Integer(required=True)
    user = fields.Nested(UserSchema)

class OnlyVehicleSchema(ma.Schema):
    """
    User Schema
    """
    vehicleID = fields.Integer()
    vehicleBrand = fields.String(required=True)
    vehicleModel = fields.String(required=True)
    rentalStatus = fields.String(required=True)
    colour = fields.String(required=True)
    seats = fields.Integer(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    cost = fields.Integer(required=True)
    userID = fields.Integer()

class RecordsSchema(ma.Schema):
    recordsID = fields.Integer()
    dateRented = fields.String(required=True)
    vehicle = fields.Nested(VehicleSchema)
    user = fields.Nested(UserSchema)

# Init schema
record_schema = RecordsSchema()
records_schema = RecordsSchema(many=True)
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)
only_vehicle_schema = OnlyVehicleSchema()
only_vehicles_schema = OnlyVehicleSchema(many=True)

# Endpoint to show all users.
@api.route("/admin/<adminUsername>", methods = ["GET"])
def get_admin(adminUsername):
    admin = Admin.query.get(adminUsername)
    return admin_schema.jsonify(admin)

# Endpoint to show all users.
@api.route("/admin", methods = ["GET"])
def get_admins():
    all_Admins = Admin.query.all()
    result = admins_schema.dump(all_Admins)
    return jsonify(result)

# Endpoint to show all users.
@api.route("/users", methods = ["GET"])
def get_users():
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/vehicles', methods=["GET"])
def get_vehicles():
    all_vehicles = Vehicle.query.all()
    result = vehicles_schema.dump(all_vehicles)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/records', methods=["GET"])
def get_records():
    all_records = Records.query.all()
    result = records_schema.dump(all_records)
    return jsonify(result)

@api.route('/onlyVehicles', methods=["GET"])
def get_only_vehicles():
    all_vehicles = Vehicle.query.all()
    result = only_vehicles_schema.dump(all_vehicles)
    return jsonify(result)
