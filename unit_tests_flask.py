import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Ensure flask was set up correctly
    def test_setup(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Welcome' in response.data)
        
    def test_admin_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login' in response.data)
    
    def test_engineer_login(self):
        tester = app.test_client(self)
        response = tester.get('/login_engineer', content_type='html/text')
        self.assertTrue(b'Login' in response.data)
    
    def test_manager_login(self):
        tester = app.test_client(self)
        response = tester.get('/login_manager', content_type='html/text')
        self.assertTrue(b'Login' in response.data)
    
    def logout(self):
        tester = app.test_client(self)
        return tester.get('/logout',follow_redirects=True)
    
    def test_login_admin_valid(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="TestAdmin", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Welcome, TestAdmin' in response.data)
    
    def test_login_admin_invalid_password(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="TestAdmin", password="Testing123"),follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)
    
    def test_login_admin_invalid_username(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="Incorrect", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)
    
    def test_login_admin_null(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="", password=""),follow_redirects=True)
        self.assertTrue(b'Login' in response.data)
    
    def test_login_manager_valid(self):
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(username="TestManager", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Welcome, TestManager' in response.data)
    
    def test_login_manager_invalid_password(self):
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(username="TestManager", password="Testing123"),follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)
    
    def test_login_manager_invalid_username(self):
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(username="Incorrect", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)
    
    def test_login_manager_null(self):
        tester = app.test_client(self)
        response = tester.post('/login_manager', data=dict(username="", password=""),follow_redirects=True)
        self.assertTrue(b'Login' in response.data)
    
    def test_login_engineer_valid(self):
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(username="TestEngineer", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Welcome, TestEngineer' in response.data)
    
    def test_login_engineer_invalid_password(self):
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(username="TestEngineer", password="Testing123"),follow_redirects=True)
        self.assertTrue(b'Password incorrect!!!' in response.data)
    
    def test_login_engineer_invalid_username(self):
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(username="Incorrect", password="Testing@123"),follow_redirects=True)
        self.assertTrue(b'Username incorrect!!!' in response.data)
    
    def test_login_engineer_null(self):
        tester = app.test_client(self)
        response = tester.post('/login_engineer', data=dict(username="", password=""),follow_redirects=True)
        self.assertTrue(b'Login' in response.data)
    
    
        
if __name__ == "__main__":
    app.secret_key='secret123'
    unittest.main()