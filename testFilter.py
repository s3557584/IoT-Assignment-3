from requestsUtil import requestsUtil
import simplejson as json
objRec = requestsUtil()
data = objRec.get_vehicles()
def search(name, field):
    for p in data:
        if p[field] == name:
            return p
value = 'colour'

results = objRec.search('White','colour',data)
print(results)
foo = {'m': {'a': 10}, 'n': {'a': 20}}

result = [v for v in foo.values() if 10 in v.values()]
