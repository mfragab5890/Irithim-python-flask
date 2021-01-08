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
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }

        self.new_user_2 = {
            'user_name': 'user_2',
            'email': 'user_1@example.com',
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_3 = {
            'user_name': 'user_1',
            'email': 'user_3@example.com',
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_4 = {
            'user_name': 'user_4',
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_5 = {
            'user_name': 'user_5',
            'email': 'user_5@example.com',
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }
        self.new_user_6 = {
            'user_name': 'user_6',
            'email': 'user_6@example.com',
            'password_hash': 'djbvjshvhzxjvhzxmbv,zxb',
            'role': True
        }

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
        res = self.client().post('/register', json=self.new_user_1)
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
