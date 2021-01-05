# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from src.models.models import *
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response




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

