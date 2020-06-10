import unittest
from requestsUtil import requestsUtil
obj = requestsUtil()
class Tests(unittest.TestCase):

    """
    Task D: Unit Test
    
    Written by: Ching Loo(s3557584)
    
    This class contains the code for unit tests in this assignment
    """
    #test_getVehicle is testing the view booked car function    
    def test_get_admin(self):
        result = obj.get_admin("TestAdmin")
        self.assertTrue(result)
    
    def test_get_engineer(self):
        result = obj.get_engineer("TestEngineer")
        self.assertTrue(result)
    
    def test_get_manager(self):
        result = obj.get_manager("TestManager")
        self.assertTrue(result)

    def test_get_user(self):
        result = obj.get_user(11)
        self.assertTrue(result)
    
    def test_get_vehicle(self):
        result = obj.get_vehicle(1)
        self.assertTrue(result)
    
    def test_get_records(self):
        result = obj.get_records()
        self.assertTrue(result)
    
    def test_get_vehicles(self):
        result = obj.get_vehicles()
        self.assertTrue(result)
    
    def test_get_users(self):
        result = obj.get_users()
        self.assertTrue(result)
    
    def test_get_engineers(self):
        result = obj.get_engineers()
        self.assertTrue(result)
    
    def test_get_maintenance(self):
        result = obj.get_maintenance()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()