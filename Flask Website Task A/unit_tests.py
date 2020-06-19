import unittest
from requestsUtil import requestsUtil
obj = requestsUtil()


class Tests(unittest.TestCase):

    """
    Task D: Unit Test

    Written by: Ching Loo(s3557584)

    This class contains the code for unit tests in this assignment mainly for testing request functions in requestUtil and the API
    """
    # test_getVehicle is testing the view booked car function

    def test_get_admin(self):
        """
        To test get_admin function
        """
        result = obj.get_admin("TestAdmin")
        self.assertTrue(result)

    def test_get_engineer(self):
        """
        To test get_engineer function
        """
        result = obj.get_engineer("TestEngineer")
        self.assertTrue(result)

    def test_get_manager(self):
        """
        To test get_manager function
        """
        result = obj.get_manager("TestManager")
        self.assertTrue(result)

    def test_get_user(self):
        """
        To test get_user function
        """
        result = obj.get_user(11)
        self.assertTrue(result)

    def test_get_vehicle(self):
        """
        To test get_vehicle function
        """
        result = obj.get_vehicle(1)
        self.assertTrue(result)

    def test_get_records(self):
        """
        To test get_records function
        """
        result = obj.get_records()
        self.assertTrue(result)

    def test_get_vehicles(self):
        """
        To test get_vehicles function
        """
        result = obj.get_vehicles()
        self.assertTrue(result)

    def test_get_users(self):
        """
        To test get_users function
        """
        result = obj.get_users()
        self.assertTrue(result)

    def test_get_engineers(self):
        """
        To test get_engineers function
        """
        result = obj.get_engineers()
        self.assertTrue(result)

    def test_get_maintenance(self):
        """
        To test get_maintenance function
        """
        result = obj.get_maintenance()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
