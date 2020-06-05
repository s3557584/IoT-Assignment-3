import simplejson as json
import requests
class requestsUtil:
        def __init__(self, url = None):
                self.url = url
                
        def get_admin(self):
                result = "http://127.0.0.1:8000/admin/" + str(self.url)
                response = requests.get(result)
                data = response.content
                data_dict = json.loads(data)
                return data_dict
        
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
        
        def search(self, name, field, responseData):
                keyValList = [name]
                results = [d for d in responseData if d[field] in keyValList]
                return results