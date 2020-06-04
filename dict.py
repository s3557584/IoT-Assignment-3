from requestsUtil import requestsUtil

objRec = requestsUtil()

testData = objRec.get_records()
for x in testData:
    print(x['dateRented'])
    print(x['user'].get('username', ''))
    print(x['vehicle'].get('vehicleBrand', ''))
    print(x['vehicle'].get('vehicleModel', ''))

