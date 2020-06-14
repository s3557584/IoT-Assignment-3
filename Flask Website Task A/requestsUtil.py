"""
Task A

Written by Ching Loo s3557584

requestUtil class

This class mainly has the code for handling GET,POST,PUT and DELETE requests through the RESTful API
"""
import simplejson as json
import requests
import re
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class requestsUtil:
    def __init__(self, url=None):
        """
        Constructor of the class

        Parameters: 
            url(str): Default is None

        Returns:
            None
        """
        self.url = url

    def get_admin(self, username):
        """
        get_admin function: Makes a GET request to API to retrieve admin data from database

        Parameters: 
            username(str): admin username

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/admin/" + username
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def get_engineer(self, username):
        """
        get_engineer function: Makes a GET request to API to retrieve engineer data from database

        Parameters: 
            username(str): engineer username

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/engineer/" + username
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def get_manager(self, username):
        """
        get_manager function: Makes a GET request to API to retrieve manager data from database

        Parameters: 
            username(str): manager username

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/manager/" + username
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def get_user(self, id):
        """
        get_user function: Makes a GET request to API to retrieve user data from database

        Parameters: 
            id(Integer): user ID

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/user/" + str(id)
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def get_vehicle(self, id):
        """
        get_vehicle function: Makes a GET request to API to retrieve vehicle data from database

        Parameters: 
            id(Integer): vehicle ID

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/vehicle/" + str(id)
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def update_user(self, id, username, firstname, surname, password, imageName):
        """
        update_user function: Makes a PUT request to API to update user data in database

        Parameters: 
            id(Integer): user ID
            username(str): User username
            firstname(str): User first name
            surname(str): User surname
            password(str): User password
            imageName(str): User image name

        Returns:
            None
        """
        result = "http://127.0.0.1:8000/user/" + str(id)
        response = requests.put(result, json={'username': username, 'firstname': firstname,
                                              'surname': surname, 'password': password, 'imageName': imageName})
        print(response)

    def update_vehicle(self, id, brand, colour, cost, seats, model):
        """
        update_vehicle function: Makes a PUT request to API to update vehicle data in database

        Parameters: 
            id(Integer): Vehicle ID
            brand(str): Vehicle brand
            colour(str): Vehicle colour
            cost(Integer): Vehicle rental rate
            seats(Integer): Vehicle number of seats
            model(str): Vehicle model

        Returns:
            None
        """
        result = "http://127.0.0.1:8000/vehicle/" + str(id)
        response = requests.put(result, json={'vehicleBrand': brand, 'colour': colour, 'cost': cost,
                                              'latitude': None, 'longitude': None, 'rentalStatus': True, 'seats': seats, 'vehicleModel': model})
        print(response)

    def get_records(self):
        """
        get_records function: Makes a GET request to API to retrieve rental records data from database

        Parameters: 
            None

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/records"
        response = requests.get(result)
        data = response.content
        data_dict = json.loads(data)
        return data_dict

    def get_vehicles(self):
        """
        get_vehicles function: Makes a GET request to API to retrieve all vehicle data from database

        Parameters: 
            None

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/onlyVehicles"
        response = requests.get(result)
        data = response.content

        data_dict = json.loads(data)
        return data_dict

    def get_users(self):
        """
        get_users function: Makes a GET request to API to retrieve all users data from database

        Parameters: 
            None

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/users"
        response = requests.get(result)
        data = response.content

        data_dict = json.loads(data)
        return data_dict

    def get_engineers(self):
        """
        get_engineers function: Makes a GET request to API to retrieve all engineers data from database

        Parameters: 
            None

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/engineers"
        response = requests.get(result)
        data = response.content

        data_dict = json.loads(data)
        return data_dict

    def get_maintenance(self):
        """
        get_maintenance function: Makes a GET request to API to retrieve all maintenance data from database

        Parameters: 
            None

        Returns:
            return data_dict: GET request result
        """
        result = "http://127.0.0.1:8000/maintenance"
        response = requests.get(result)
        data = response.content

        data_dict = json.loads(data)
        return data_dict

    def add_user(self, username, firstname, surname, password, imageName):
        """
        add_user function: Makes a POST request to API to insert user data in database

        Parameters: 
            id(Integer): user ID
            username(str): User username
            firstname(str): User first name
            surname(str): User surname
            password(str): User password
            imageName(str): User image name

        Returns:
            None
        """
        url = "http://127.0.0.1:8000/user"
        response = requests.post(url, json={'username': username, 'firstname': firstname,
                                            'surname': surname, 'password': password, 'imageName': imageName})
        print(response)

    def add_vehicle(self, brand, colour, cost, seats, model):
        """
        add_vehicle function: Makes a POST request to API to add vehicle data in database

        Parameters: 
            id(Integer): Vehicle ID
            brand(str): Vehicle brand
            colour(str): Vehicle colour
            cost(Integer): Vehicle rental rate
            seats(Integer): Vehicle number of seats
            model(str): Vehicle model

        Returns:
            None
        """
        url = "http://127.0.0.1:8000/vehicle"
        response = requests.post(url, json={'brand': brand, 'colour': colour, 'cost': cost, 'latitude': None,
                                            'longitude': None, 'status': True, 'seats': seats, 'id': None, 'model': model})
        print(response)

    def add_maintenance(self, vehicleID, vehicleModel, longitude, latitude, engineerName, engineerDevice, engineerDeviceID):
        """
        add_maintenance function: Makes a POST request to API to add maintenance data in database

        Parameters: 
            vehicleID(Integer): Vehicle ID
            longitude(float): Longitude location of vehicle
            latitude(float): Latitude location of vehicle
            engineerName(str): Engineer Username
            engineerDevice(str): Engineer mobile device name
            engineerDeviceID(Integer): MAC address of engineer's device
            vehicleModel(str): Vehicle model

        Returns:
            None
        """
        url = "http://127.0.0.1:8000/maintenance"
        response = requests.post(url, json={'vehicleID': vehicleID, 'model': vehicleModel, 'longitude': longitude,
                                            'latitude': latitude, 'engineerName': engineerName, 'engineerDevice': engineerDevice, 'engineerDeviceID': engineerDeviceID})
        print(response)

    def delete_vehicle(self, id):
        """
        delete_vehicle function: Makes a DELETE request to API to delete vehicle data from database

        Parameters: 
            id(Integer): Vehicle ID

        Returns:
            None
        """
        url = "http://127.0.0.1:8000/deleteVehicle/" + str(id)
        response = requests.delete(url)
        print(response)

    def delete_user(self, id):
        """
        delete_user function: Makes a DELETE request to API to delete user data from database

        Parameters: 
            id(Integer): User ID

        Returns:
            None
        """
        url = "http://127.0.0.1:8000/deleteUser/" + str(id)
        response = requests.delete(url)
        print(response)

    def search(self, name, field, responseData):
        """
        search function to filter data from dictionary

        Parameters: 
            name(str): username
            field(str): category
            respondData(dictionary): Dictionary result from API requests 

        Returns:
            results(dictionary): returns filtered result
        """
        keyValList = [name]
        results = [d for d in responseData if d[field] in keyValList]
        return results

    def generate_key(self):
        """
        generate_key function to generate key for encryption and decryption

        Parameters: 
            None 

        Returns:
            key(bytes): key generate to use for encryption and decryption
        """
        password = b"password"
        salt = b'Oy\nK5o\x15\xa8ex2U\x94A\xb9\x8c'
        kdf = PBKDF2HMAC(

            algorithm=hashes.SHA256(),

            length=32,

            salt=salt,

            iterations=100000,

            backend=default_backend()

        )

        key = base64.urlsafe_b64encode(kdf.derive(password))

        return key

    def encryptPassword(self, password):
        """
        Function to encrypt password

        Parameters:
                password(str): Plaintext password from user input

        Returns:
                encrypted(byte): Encrypted password
        """
        f = Fernet(self.generate_key())
        encrypted = f.encrypt(password.encode('utf-8'))
        return encrypted

    def decryptPassword(self, encrypted_password):
        """
        Function to decrypt encrypted password

        Parameters:
                encrypted_password(byte): ciphertext password from database

        Returns:
                password(str): plaintext password
        """
        f = Fernet(self.generate_key())
        toDecrypt = encrypted_password.encode('utf-8')
        decrypted = f.decrypt(toDecrypt)
        password = decrypted.decode('utf-8')

        return password
