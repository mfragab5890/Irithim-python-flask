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
        self.bad_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiQWRtaW4iLCJwZXJtaXNzaW9ucyI6eyJnZXRfYWxsX2xpc3RzIjpmYWxzZSwiY3JlYXRlX2xpc3QiOmZhbHNlLCJ1cGRhdGVfbGlzdCI6ZmFsc2UsImRlbGV0ZV9saXN0IjpmYWxzZSwiZ2V0X2xpc3QiOmZhbHNlLCJhc3NpZ25fbWVtYmVyX2xpc3QiOmZhbHNlLCJyZXZva2VfbWVtYmVyX2xpc3QiOmZhbHNlLCJnZXRfYWxsX3VzZXJzIjpmYWxzZSwiY3JlYXRlX2NhcmQiOmZhbHNlLCJ1cGRhdGVfY2FyZCI6ZmFsc2UsImRlbGV0ZV9jYXJkIjpmYWxzZSwiZ2V0X2NhcmQiOmZhbHNlLCJjcmVhdGVfY29tbWVudCI6ZmFsc2UsInVwZGF0ZV9jb21tZW50IjpmYWxzZSwiZGVsZXRlX2NvbW1lbnQiOmZhbHNlLCJnZXRfY29tbWVudCI6ZmFsc2UsImNyZWF0ZV9yZXBsaWVzIjpmYWxzZSwidXBkYXRlX3JlcGxpZXMiOmZhbHNlLCJkZWxldGVfcmVwbGllcyI6ZmFsc2UsImdldF9yZXBsaWVzIjpmYWxzZX19.KQtBc_SiindvMVTumfzmQ9bcg-QPlFPaKJbOHMJ7JjU'
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
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/unconfirmed')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data[ 'users' ])

    # test error get unconfirmed users from database with forbidden token
    def test_error_get_unconfirmed_users(self):
        """Test error query unconfirmed users will not return results with forbidden key token """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 2
                sess[ 'token' ] = self.bad_token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/unconfirmed')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data[ 'success' ], False)
            self.assertEqual(data[ 'message' ], 'Unauthorized.')

    # test get users per page from database
    def test_get_users_per_page(self):
        """Test query users will return results paginated """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/users/1')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data[ 'users' ])

    # test error get users from database with no page parameter
    def test_error_get_users_no_page(self):
        """Test query unconfirmed users will return results """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/users')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data[ 'success' ], False)
            self.assertEqual(data[ 'message' ],
                             'Not found!!! : please check your Data or maybe your request is currently not available.')

    # test error get users from database with forbidden token
    def test_error_get_users_bad_token(self):
        """Test error query users will not return results with forbidden key token """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 2
                sess[ 'token' ] = self.bad_token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/users/1')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data[ 'code' ], 'permission_access_forbidden')
            self.assertEqual(data[ 'description' ], 'Access to this entity is forbidden.')

    # test get lists per page from database
    def test_get_lists_per_page(self):
        """Test query lists will return results paginated """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/lists/1')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data[ 'lists' ])

    # test error get lists from database with forbidden token
    def test_error_get_lists_bad_token(self):
        """Test error query lists will not return results with forbidden key token """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 2
                sess[ 'token' ] = self.bad_token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/users/1')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data[ 'code' ], 'permission_access_forbidden')
            self.assertEqual(data[ 'description' ], 'Access to this entity is forbidden.')

    # test get list by id from database
    def test_get_user_list(self):
        """Test query list by id will return results"""
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/list', json={'list_id':1})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data[ 'list' ])

    # test error get list by id from database with forbidden token
    def test_error_get_list_bad_token(self):
        """Test error query list will not return results with forbidden key token """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 2
                sess[ 'token' ] = self.bad_token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/list', json={'list_id':1})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data[ 'code' ], 'permission_access_forbidden')
            self.assertEqual(data[ 'description' ], 'Access to this entity is forbidden.')

    # test get all cards from database
    def test_get_all_cards(self):
        """Test query all cards will return results paginated """
        with self.client() as c:
            with c.session_transaction() as sess:
                sess[ 'user_id' ] = 1
                sess[ 'token' ] = self.token
            c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
            res = c.get('/cards/1')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data[ 'cards' ])

    # test error get list by id from database with forbidden token
    def test_error_get_list_bad_token(self):
        """Test error query list will not return results with forbidden key token """
        with self.client() as c:
            with self.client() as c:
                with c.session_transaction() as sess:
                    sess[ 'user_id' ] = 1
                    sess[ 'token' ] = self.bad_token
                c.set_cookie('localhost', 'MYCOOKIE', 'cookie_value')
                res = c.get('/cards/1')
                data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data[ 'code' ], 'permission_access_forbidden')
            self.assertEqual(data[ 'description' ], 'Access to this entity is forbidden.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
