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
    Admin Class/Model
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
    """
    Records Class/Model
    """
    recordsID = db.Column(db.Integer, primary_key=True)
    dateRented = db.Column(db.String(100))
    vehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.vehicleID'), nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=True)
    daysRented = db.Column(db.Integer)
    user = db.relationship("User", backref="userTable")
    vehicle = db.relationship("Vehicle", backref="vehicleTable")
    def __init__(self, dateRented, vehicleID, userID, daysRented):
        self.dateRented = dateRented
        self.vehicleID = vehicleID
        self.userID = userID
        self.daysRented = daysRented

class Maintenance(db.Model):
    """
    Maintenance Class/Model
    """
    maintenanceID = db.Column(db.Integer, primary_key=True)
    vehicleID = db.Column(db.Integer)
    vehicleModel = db.Column(db.String(100))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    engineerName = db.Column(db.String(100))
    engineerDevice = db.Column(db.String(100))
    engineerDeviceID = db.Column(db.String(100))

    def __init__(self, vehicleID, vehicleModel, longitude, latitude, engineerName, engineerDevice, engineerDeviceID):
        self.vehicleID = vehicleID
        self.vehicleModel = vehicleModel
        self.longitude = longitude
        self.latitude = latitude
        self.engineerName = engineerName
        self.engineerDevice = engineerDevice
        self.engineerDeviceID = engineerDeviceID

class Engineer(db.Model):
    """
    Engineer Class/Model
    """
    engineerUsername = db.Column(db.String(100), primary_key=True)
    engineerName = db.Column(db.String(100))
    engineerPassword = db.Column(db.String(1111))
    engineerDevice = db.Column(db.String(100))
    engineerDeviceID = db.Column(db.String(100))
    
    def __init__(self, engineerUsername, engineerName, engineerPassword, engineerDevice, engineerDeviceID):
        self.engineerUsername = engineerUsername
        self.engineerName = engineerName
        self.engineerPassword = engineerPassword
        self.engineerDevice = engineerDevice
        self.engineerDeviceID = engineerDeviceID

class Manager(db.Model):
    """
    Manager Class/Model
    """
    managerUsername = db.Column(db.String(100), primary_key=True)
    managerName = db.Column(db.String(100))
    managerPassword = db.Column(db.String(1111))
    
    def __init__(self, managerUsername, managerName, managerPassword):
        self.managerUsername = managerUsername
        self.managerName = managerName
        self.managerPassword = managerPassword

class AdminSchema(ma.Schema):
    """
    Admin Schema
    """
    adminUsername = fields.String(required=True)
    adminName = fields.String(required=True)
    adminPassword = fields.String(required=True)

class EngineerSchema(ma.Schema):
    """
    Engineer Schema
    """
    engineerUsername = fields.String(required=True)
    engineerName = fields.String(required=True)
    engineerPassword = fields.String(required=True)
    engineerDevice = fields.String(required=True)
    engineerDeviceID = fields.String(required=True)

class ManagerSchema(ma.Schema):
    """
    Manager Schema
    """
    managerUsername = fields.String(required=True)
    managerName = fields.String(required=True)
    managerPassword = fields.String(required=True)

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
    Vehicle Schema
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
    Only vehicle Schema
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
    """
    Records Schema
    """
    recordsID = fields.Integer()
    dateRented = fields.String(required=True)
    daysRented = fields.Integer()
    vehicle = fields.Nested(VehicleSchema)
    user = fields.Nested(UserSchema)

class UpdateAddUserSchema(ma.Schema):
    """
    UpdateAddUser schema
    """
    class Meta:
        # Fields to expose
        fields = ('userID','username', 'firstname', 'surname', 'password', 'imageName')

class MaintenanceSchema(ma.Schema):
    """
    Maintenance schema
    """
    class Meta:
        # Fields to expose
        fields = ('vehicleID','userID','vehicleModel', 'longitude', 'latitude', 'engineerName', 'engineerDeviceID')

class UpdateAddVehicleSchema(ma.Schema):
    """
    UpdateAddVehicle Schema
    """
    class Meta:
        fields = ('vehicleID', 'vehicleBrand', 'vehicleModel', 'rentalStatus', 'colour', 'seats', 'latitude', 'longitude', 'cost', 'userID')


# Init schema
record_schema = RecordsSchema()
records_schema = RecordsSchema(many=True)
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
admin_schema = AdminSchema()
manager_schema = ManagerSchema()
engineer_schema = EngineerSchema()
engineers_schema = EngineerSchema(many=True)
admins_schema = AdminSchema(many=True)
only_vehicle_schema = OnlyVehicleSchema()
only_vehicles_schema = OnlyVehicleSchema(many=True)
update_add_user_Schema = UpdateAddUserSchema()
update_add_vehicle_schema = UpdateAddVehicleSchema()
maintenance_schema = MaintenanceSchema()
maintenances_schema = MaintenanceSchema(many=True)

# Endpoint to get specific admin.
@api.route("/admin/<adminUsername>", methods = ["GET"])
def get_admin(adminUsername):
    """
    Endpoint for getting admin details from db

    Parameters:
        adminUsername(str): Admin username
    
    Returns:
        return admin_schema.jsonify(admin): returns result
    """
    admin = Admin.query.get(adminUsername)
    return admin_schema.jsonify(admin)

# Endpoint to show all users.
@api.route("/engineer/<engineerUsername>", methods = ["GET"])
def get_engineer(engineerUsername):
    """
    Endpoint for getting engineer details from db

    Parameters:
        engineerUsername(str): Engineer username
    
    Returns:
        return engineer_schema.jsonify(engineer): returns result
    """
    engineer = Engineer.query.get(engineerUsername)
    return engineer_schema.jsonify(engineer)

@api.route("/manager/<managerUsername>", methods = ["GET"])
def get_manager(managerUsername):
    """
    Endpoint for getting manager details from db

    Parameters:
        managerUsername(str): Manager username
    
    Returns:
        return manager_schema.jsonify(manager): returns result
    """
    manager = Manager.query.get(managerUsername)
    return manager_schema.jsonify(manager)

# Endpoint to show all users.
@api.route("/user/<userID>", methods = ["GET"])
def get_user(userID):
    """
    Endpoint for getting user details from db

    Parameters:
        userID(Integer): Manager username
    
    Returns:
        return user_schema.jsonify(admin): returns result
    """
    admin = User.query.get(userID)
    return user_schema.jsonify(admin)

# Endpoint to show all users.
@api.route("/vehicle/<vehicleID>", methods = ["GET"])
def get_vehicle(vehicleID):
    """
    Endpoint for getting vehicle details from db

    Parameters:
        vehicleID(Integer): Vehicle ID
    
    Returns:
        return update_add_vehicle_schema.jsonify(admin): returns result
    """
    admin = Vehicle.query.get(vehicleID)
    return update_add_vehicle_schema.jsonify(admin)

# Create a User
@api.route('/user/<userID>', methods=['PUT'])
def update_user(userID):
    """
    Endpoint for updating user details from db

    Parameters:
        userID(Integer): User ID
    
    Returns:
        return update_add_user_Schema.jsonify(user): returns result
    """
    user = User.query.get(userID)
    username = request.json['username']
    firstname = request.json['firstname']
    surname = request.json['surname']
    password = request.json['password']
    imageName = request.json['imageName']

    user.username = username
    user.firstname = firstname
    user.surname = surname
    user.password = password
    user.imageName = imageName

    db.session.commit()
    return update_add_user_Schema.jsonify(user)


@api.route('/user', methods=['POST'])
def add_user():
    """
    Endpoint for adding new user to db

    Parameters:
        None
    
    Returns:
        return update_add_user_Schema.jsonify(new_user): returns result
    """
    username = request.json['username']
    firstname = request.json['firstname']
    surname = request.json['surname']
    password = request.json['password']
    imageName = request.json['imageName']

    new_user = User(username, firstname, surname, password, imageName)

    db.session.add(new_user)
    db.session.commit()

    return update_add_user_Schema.jsonify(new_user)

# Create a Vehicle
@api.route('/vehicle', methods=['POST'])
def add_vehicle():
    """
    Function to add a Vehicle
    
    Parameters:
        None
		
    Returns:
        vehicle_schema.jsonify(new_vehicle): convert received data to json format
    """
    vehicleBrand = request.json['brand']
    vehicleModel = request.json['model']
    rentalStatus = request.json['status']
    colour = request.json['colour']
    seats = request.json['seats']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    cost = request.json['cost']
    userID = request.json['id']

    new_vehicle = Vehicle(vehicleBrand, vehicleModel, rentalStatus, colour, seats, latitude, longitude, cost, userID)

    db.session.add(new_vehicle)
    db.session.commit()

    return vehicle_schema.jsonify(new_vehicle)

# Create a Vehicle
@api.route('/maintenance', methods=['POST'])
def add_maintenance():
    """
    Endpoint for adding new maintenance details to db

    Parameters:
        None
    
    Returns:
       return vehicle_schema.jsonify(new_maintenance): returns result
    """
    vehicleID = request.json['vehicleID']
    vehicleModel = request.json['model']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    engineerName = request.json['engineerName']
    engineerDevice = request.json['engineerDevice']
    engineerDeviceID = request.json['engineerDeviceID']

    new_maintenance = Maintenance(vehicleID, vehicleModel, longitude, latitude, engineerName, engineerDevice, engineerDeviceID)

    db.session.add(new_maintenance)
    db.session.commit()

    return vehicle_schema.jsonify(new_maintenance)

@api.route('/vehicle/<vehicleID>', methods=['PUT'])
def update_vehicle(vehicleID):
    """
    Endpoint for updating vehicle details from db

    Parameters:
        vehicleID(Integer): Vehicle ID
    
    Returns:
         return update_add_vehicle_schema.jsonify(vehicle): returns result
    """
    vehicle = Vehicle.query.get(vehicleID)
    vehicleBrand = request.json['vehicleBrand']
    vehicleModel = request.json['vehicleModel']
    rentalStatus = request.json['rentalStatus']
    colour = request.json['colour']
    seats = request.json['seats']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    cost = request.json['cost']
    

    vehicle.vehicleBrand = vehicleBrand
    vehicle.vehicleModel = vehicleModel
    vehicle.rentalStatus = rentalStatus
    vehicle.colour = colour
    vehicle.seats = seats
    vehicle.latitude = latitude
    vehicle.longitude = longitude
    vehicle.cost = cost


    db.session.commit()

    return update_add_vehicle_schema.jsonify(vehicle)

# Endpoint to show all users.
@api.route("/admin", methods = ["GET"])
def get_admins():
    """
    Endpoint for getting all admin details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_Admins = Admin.query.all()
    result = admins_schema.dump(all_Admins)
    return jsonify(result)

# Endpoint to show all users.
@api.route("/users", methods = ["GET"])
def get_users():
    """
    Endpoint for getting all user details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/vehicles', methods=["GET"])
def get_vehicles():
    """
    Endpoint for getting all vehicle details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_vehicles = Vehicle.query.all()
    result = vehicles_schema.dump(all_vehicles)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/records', methods=["GET"])
def get_records():
    """
    Endpoint for getting all records details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_records = Records.query.all()
    result = records_schema.dump(all_records)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/engineers', methods=["GET"])
def get_engineers():
    """
    Endpoint for getting all engineer details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_engineers = Engineer.query.all()
    result = engineers_schema.dump(all_engineers)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/maintenance', methods=["GET"])
def get_maintenance():
    """
    Endpoint for getting all maintenance details from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_maintenance = Maintenance.query.all()
    result = maintenances_schema.dump(all_maintenance)
    return jsonify(result)

@api.route('/onlyVehicles', methods=["GET"])
def get_only_vehicles():
    """
    Endpoint for getting all vehicle details excluding the foreign keys info from db

    Parameters:
        None
    
    Returns:
        return jsonify(result): returns result
    """
    all_vehicles = Vehicle.query.all()
    result = only_vehicles_schema.dump(all_vehicles)
    return jsonify(result)

@api.route('/deleteVehicle/<vehicleID>', methods=["DELETE"])
def delete_vehicle(vehicleID):
    """
    Endpoint for deleting vehicle details from db

    Parameters:
        None
    
    Returns:
       return vehicle_schema.jsonify(vehicle): returns result
    """
    vehicle = Vehicle.query.get(vehicleID)
    db.session.delete(vehicle)
    db.session.commit()

    return vehicle_schema.jsonify(vehicle)

@api.route('/deleteUser/<userID>', methods=["DELETE"])
def delete_user(userID):
    """
    Endpoint for deleting user details from db

    Parameters:
        None
    
    Returns:
         return user_schema.jsonify(user): returns result
    """
    user = User.query.get(userID)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)