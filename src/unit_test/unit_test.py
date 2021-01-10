import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src.app import create_app
from src.models.models import *


class IrithmTestCase(unittest.TestCase):
    """This class represents the irithm test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'irithm_test'
        setup_db(self.app, self.database_name)

        self.new_user_1 = {
            'user_name': 'user_1',
            'email': 'user_1@example.com',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }

        self.new_user_2 = {
            'user_name': 'user_2',
            'email': 'user_1@example.com',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_3 = {
            'user_name': 'user_1',
            'email': 'user_3@example.com',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_4 = {
            'user_name': 'user_4',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_5 = {
            'user_name': 'user_5',
            'email': 'user_5@example.com',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_6 = {
            'user_name': 'user_6',
            'email': 'user_6@example.com',
            'password': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.login_user_false = {
            "email": "m.f.ragab5890@gmail.com",
            "password": "tafTAFI",
            "user_name": "mostafa_ragab"
        }
        self.login_user_true = {
            "email": "m.f.ragab5890@gmail.com",
            "password": "tafiTAFI",
            "user_name": "mostafa_ragab"
        }
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiQWRtaW4iLCJwZXJtaXNzaW9ucyI6eyJnZXRfYWxsX2xpc3RzIjoiQWxsIiwiY3JlYXRlX2xpc3QiOiJBbGwiLCJ1cGRhdGVfbGlzdCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZGVsZXRlX2xpc3QiOlsxLDIsMyw0LDUsNiw3LDgsOSwxMF0sImdldF9saXN0IjoiQWxsIiwiYXNzaWduX21lbWJlcl9saXN0IjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJyZXZva2VfbWVtYmVyX2xpc3QiOlsxLDIsMyw0LDUsNiw3LDgsOSwxMF0sImdldF9hbGxfdXNlcnMiOiJBbGwiLCJjcmVhdGVfY2FyZCI6IkFsbCIsInVwZGF0ZV9jYXJkIjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfY2FyZCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X2NhcmQiOiJBbGwiLCJjcmVhdGVfY29tbWVudCI6IkFsbCIsInVwZGF0ZV9jb21tZW50IjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfY29tbWVudCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X2NvbW1lbnQiOiJBbGwiLCJjcmVhdGVfcmVwbGllcyI6IkFsbCIsInVwZGF0ZV9yZXBsaWVzIjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfcmVwbGllcyI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X3JlcGxpZXMiOiJBbGwifX0.SPGXta7MX1hDVmi2jOXR33pexRc7M9GJ9cWEZLGKQn8'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all(app=create_app())

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test add a new user to database
    def test_register_user(self):
        """Test if when registering a user it will be added successfully """
        res = self.client().post('/register', json=self.new_user_6)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[ 'success' ], True)
        self.assertTrue(data[ 'message' ], 'User created successfully, Please wait for owner to confirm')

    # test error while registering a new user with used user name
    def test_error_user_duplicate_user_name(self):
        """Test if user if error will occur on user submit used user name """
        res = self.client().post('/register', json=self.new_user_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data[ 'success' ], False)
        self.assertEqual(data[ 'message' ],
                         'Unprocessable!!! : The request was well-formed but was unable to be followed')

    # test error while registering a new user with used user name
    def test_error_user_duplicate_email(self):
        """Test if user if error will occur on user submit used email """
        res = self.client().post('/register', json=self.new_user_3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data[ 'success' ], False)
        self.assertEqual(data[ 'message' ],
                         'Unprocessable!!! : The request was well-formed but was unable to be followed')

    # test error while logging in with false credetials
    def test_error_user_login(self):
        """Test if error will occur on user submit wrong credentials upon login """
        res = self.client().post('/login', json=self.login_user_false)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data[ 'success' ], False)
        self.assertEqual(data[ 'message' ], 'Unauthorized.')

    # test login with right credentials will succeed
    def test_user_login(self):
        """Test right credentials upon login will give access to the user """
        res = self.client().post('/login', json=self.login_user_true)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[ 'success' ], True)
        self.assertEqual(data[ 'message' ], 'logged in successfully')

    # test get unconfirmed users from database
    def test_get_unconfirmed_users(self):
        """Test query unconfirmed users will return results """
        with self.app.test_client() as tclient:
            with tclient.session_transaction() as sess:
                sess[ 'token' ] = self.token
                sess['user_id'] = 1
        res = self.client().get('/unconfirmed')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
