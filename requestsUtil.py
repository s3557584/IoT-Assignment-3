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
        def __init__(self, url = None):
                self.url = url
                
        def get_admin(self, username):
                result = "http://127.0.0.1:8000/admin/" + username
                response = requests.get(result)
                data = response.content
                data_dict = json.loads(data)
                return data_dict
        
        def get_user(self, id):
                result = "http://127.0.0.1:8000/user/" + str(id)
                response = requests.get(result)
                data = response.content
                data_dict = json.loads(data)
                return data_dict
        
        def get_vehicle(self, id):
                result = "http://127.0.0.1:8000/vehicle/" + str(id)
                response = requests.get(result)
                data = response.content
                data_dict = json.loads(data)
                return data_dict
        
        def update_user(self, id, username, firstname, surname, password, imageName):
                result = "http://127.0.0.1:8000/user/" + str(id)
                response = requests.put(result, json={'username':username,'firstname':firstname,'surname':surname,'password':password,'imageName':imageName})
                print(response)
        
        def update_vehicle(self, id, brand, colour, cost, seats, model):
                result = "http://127.0.0.1:8000/vehicle/" + str(id)
                response = requests.put(result, json={'vehicleBrand':brand,'colour':colour,'cost':cost,'latitude':None,'longitude':None,'rentalStatus':True,'seats':seats,'vehicleModel':model})
                print(response)
        
        def get_records(self):
                result = "http://127.0.0.1:8000/records" 
                response = requests.get(result)
                data = response.content
                data_dict = json.loads(data)
                return data_dict
        
        def get_vehicles(self):
                result = "http://127.0.0.1:8000/onlyVehicles" 
                response = requests.get(result)
                data = response.content

                data_dict = json.loads(data)
                return data_dict
        
        def get_users(self):
                result = "http://127.0.0.1:8000/users" 
                response = requests.get(result)
                data = response.content

                data_dict = json.loads(data)
                return data_dict
        
        def get_engineers(self):
                result = "http://127.0.0.1:8000/engineers" 
                response = requests.get(result)
                data = response.content

                data_dict = json.loads(data)
                return data_dict
        
        def add_user(self, username, firstname, surname, password, imageName):
                url = "http://127.0.0.1:8000/user"
                response = requests.post(url, json={'username':username,'firstname':firstname,'surname':surname,'password':password, 'imageName':imageName})
                print(response)
        
        def add_vehicle(self, brand, colour, cost, seats, model):
                url = "http://127.0.0.1:8000/vehicle"
                response = requests.post(url, json={'brand':brand,'colour':colour,'cost':cost,'latitude':None,'longitude':None,'status':True,'seats':seats,'id':None,'model':model})
                print(response)
        
        def add_maintenance(self, vehicleID, vehicleModel, longitude, latitude, engineerName, engineerDevice):
                url = "http://127.0.0.1:8000/maintenance"
                response = requests.post(url, json={'vehicleID':vehicleID,'model':vehicleModel,'longitude':longitude,'latitude':latitude,'engineerName':engineerName,'engineerDevice':engineerDevice})
                print(response)
        
        def delete_vehicle(self, id):
                url = "http://127.0.0.1:8000/deleteVehicle/" + str(id)
                response = requests.delete(url)
                print(response)
        
        def delete_user(self, id):
                url = "http://127.0.0.1:8000/deleteUser/" + str(id)
                response = requests.delete(url)
                print(response)

        def search(self, name, field, responseData):
                keyValList = [name]
                results = [d for d in responseData if d[field] in keyValList]
                return results

        def generate_key(self):
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
                Task A
                
                Written by: Ching Loo(s3557584)
                
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
                Task A
                
                Written by: Ching Loo(s3557584)
                
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