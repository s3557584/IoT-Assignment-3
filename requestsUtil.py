import simplejson as json
import requests
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
        
        def add_user(self, username, firstname, surname, password, imageName):
                url = "http://127.0.0.1:8000/user"
                response = requests.post(url, json={'username':username,'firstname':firstname,'surname':surname,'password':password, 'imageName':imageName})
                print(response)
        
        def add_vehicle(self, brand, colour, cost, seats, model):
                url = "http://127.0.0.1:8000/vehicle"
                response = requests.post(url, json={'brand':brand,'colour':colour,'cost':cost,'latitude':None,'longitude':None,'status':True,'seats':seats,'id':None,'model':model})
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