import unittest
from app import app


class FlaskTestCase(unittest.TestCase):
    """
    Task D: Unit Test

    Written by: Ching Loo(s3557584)

    This class contains the code for unit tests in this assignment mainly for the flask application part of the assignment
    """

    # Ensure flask was set up correctly
    def test_setup(self):
        """
        To test if flask is setup properly
        """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        """
        To test if index page is working or not
        """
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Welcome' in response.data)

    def test_admin_login(self):
        """
        To test if admin login page is working or not
        """
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    def test_engineer_login(self):
        """
        To test if engineer login page is working or not
        """
        tester = app.test_client(self)
        response = tester.get('/login_engineer', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    def test_manager_login(self):
        """
        To test if manager login page is working or not
        """
        tester = app.test_client(self)
        response = tester.get('/login_manager', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    def logout(self):
        """
        To test if logout function is working or not
        """
        tester = app.test_client(self)
        return tester.get('/logout', follow_redirects=True)

    def test_login_admin_valid(self):
        """
        To test if admin login function is working or not(valid info)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login', data=dict(username="TestAdmin", password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Welcome, TestAdmin' in response.data)

    def test_login_admin_invalid_password(self):
        """
        To test if admin login function is working or not(invalid password)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login', data=dict(username="TestAdmin", password="Testing123"), follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)

    def test_login_admin_invalid_username(self):
        """
        To test if admin login function is working or not(invalid username)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login', data=dict(username="Incorrect", password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)

    def test_login_admin_null(self):
        """
        To test if admin login function is working or not(no input)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login', data=dict(username="", password=""), follow_redirects=True)
        self.assertTrue(b'Login' in response.data)

    def test_login_manager_valid(self):
        """
        To test if manager login function is working or not(valid info)
        """
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(
            username="TestManager", password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Welcome, TestManager' in response.data)

    def test_login_manager_invalid_password(self):
        """
        To test if manager login function is working or not(invalid password)
        """
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(
            username="TestManager", password="Testing123"), follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)

    def test_login_manager_invalid_username(self):
        """
        To test if manager login function is working or not(invalid username)
        """
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(username="Incorrect",
                                                           password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)

    def test_login_manager_null(self):
        """
        To test if manager login function is working or not(no input)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login_manager', data=dict(username="", password=""), follow_redirects=True)
        self.assertTrue(b'Login' in response.data)

    def test_login_engineer_valid(self):
        """
        To test if engineer login function is working or not(invalid info)
        """
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(
            username="TestEngineer", password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Welcome, TestEngineer' in response.data)

    def test_login_engineer_invalid_password(self):
        """
        To test if eingineer login function is working or not(invalid password)
        """
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(
            username="TestEngineer", password="Testing123"), follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)

    def test_login_engineer_invalid_username(self):
        """
        To test if eingineer login function is working or not(invalid username)
        """
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(
            username="Incorrect", password="Testing@123"), follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)

    def test_login_engineer_null(self):
        """
        To test if eingineer login function is working or not(no input)
        """
        tester = app.test_client(self)
        response = tester.post(
            '/login_engineer', data=dict(username="", password=""), follow_redirects=True)
        self.assertTrue(b'Login' in response.data)


if __name__ == "__main__":
    app.secret_key = 'secret123'
    unittest.main()
