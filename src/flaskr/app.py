# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort, session
import json
from flask_cors import CORS
from models.models import *
from .auth import *

# creating and initializing the app.

def create_app(test_config=None):
    # ----------------------------------------------------------------------------#
    # App Config.
    # ----------------------------------------------------------------------------#
    app = Flask(__name__)
    # wrap database to app
    setup_db(app, database_name)
    # using cors with app
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    # testing app
    @app.route('/', methods=[ 'GET' ])
    def index():
        session[ 'data' ] = 1
        return str(session[ 'data' ])

    # ----------------------------------------------------------------------------#
    # owner end points.
    # ----------------------------------------------------------------------------#
    # get unconfirmed users
    # confirm users or delete sign-up request
    # change role

    # ----------------------------------------------------------------------------#
    # User end points.
    # ----------------------------------------------------------------------------#
    # sign-up endpoint
    @app.route('/register', methods=[ 'POST' ])
    def create_user():
        body = request.get_json()

        new_user_name = body.get('userName', None)
        new_email = body.get('email', None)
        new_role = body.get('role', None)
        new_password = body.get('password', None)

        try:
            if new_user_name is None or new_email is None or new_role is None or new_password is None:

                abort(400)

            else:
                user = User(user_name=new_user_name,
                            email=new_email,
                            role=new_role,
                            password=set_password(new_password)
                            )
                user.insert()

                return jsonify({
                    'success': True,
                    'message': 'User created successfully'
                })


        except Exception as e:
            abort(422)
    # get all users paginated endpoint
    # user log-in endpoint
    # get all lists paginated endpoint
    # get list by id with cards in it endpoint
    # create list endpoint
    #











    # ----------------------------------------------------------------------------#
    # Error Handlers.
    # ----------------------------------------------------------------------------#
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Not found!!! : please check your Data or maybe your request is currently not available.'
        }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable!!! : The request was well-formed but was unable to be followed'
        }), 422

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed!!!: Your request method not supported by that API '
        }), 405

    @app.errorhandler(400)
    def not_good_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request!!!! Please make sure the data you entered is correct'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error!!!: Please try again later or reload request. '
        }), 500

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above 
    '''

    @app.errorhandler(401)
    def Unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorized. '
        }), 401

    @app.errorhandler(403)
    def forbidden_access(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": 'Access to the requested resource is forbidden. '
        }), 403

    return app
