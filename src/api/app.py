# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort, session
from flask_cors import CORS
from models import models
from models import *
from flaskr import auth


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
    results_per_page = 100
    # testing app
    @app.route('/', methods=[ 'GET' ])
    def index():
        session[ 'user_id' ] = 1
        return str(session[ 'user_id' ])

    # ----------------------------------------------------------------------------#
    # owner end points.
    # ----------------------------------------------------------------------------#
    # get all unconfirmed users
    @app.route('/unconfirmed', methods=[ 'GET' ])
    def get_unconfirmed_users():
        # check if user logged in and is the owner
        if session[ 'user_id' ]:
            id = session[ 'user_id' ]
            verify = Owner.query.get(id)
            if verify is not None:
                unconfirmed_users = User_unconfirmed.query.all()
                users = [ user.format() for user in unconfirmed_users ]
                return users
            else:
                abort(401)
        else:
            abort(401)

    # confirm users
    @app.route('/user/confirmation/<int:user_id>', methods=[ 'post' ])
    def confirm_user(user_id):
        # check if user logged in and is the owner
        if session[ 'user_id' ]:
            owner_id = session[ 'user_id' ]
            verify = Owner.query.get(owner_id)
            if verify is not None:
                new_user = User_unconfirmed.query.get(user_id)
                try:
                    user = User(user_name=new_user.user_name,
                                email=new_user.email,
                                role=new_user.role,
                                password=new_user.password)

                    return jsonify({
                        'success': True,
                        'message': 'User confirmed successfully'
                    })
                except Exception as e:
                    abort(422)

    # delete sign-up request
    @app.route('/user/confirmation/<int:user_id>', methods=[ 'DELETE' ])
    def delete_user(user_id):
        # check if user logged in and is the owner
        if session[ 'user_id' ]:
            owner_id = session[ 'user_id' ]
            verify = Owner.query.get(owner_id)
            if verify is not None:
                new_user = User_unconfirmed.query.get(user_id)
                try:
                    new_user.delete()

                    return jsonify({
                        'success': True,
                        'message': 'User deleted successfully'
                    })
                except Exception as e:
                    abort(422)

    # change role
    @app.route('/user-role/<int:user_id>', methods=[ 'DELETE' ])
    def change_user_role(user_id):
        # check if user logged in and is the owner
        if session[ 'user_id' ]:
            owner_id = session[ 'user_id' ]
            verify = Owner.query.get(owner_id)
            if verify is not None:
                body = request.get_json()
                # verify user requested exists
                user = User.query.filter_by(id=user_id).one_or_none()
                if user:
                    if 'role' in body:
                        role = body.get('role')
                        if role:
                            user.role = True
                        else:
                            user.role = False

                try:
                    user.update()

                    return jsonify({
                        'success': True,
                        'message': 'User role changed successfully'
                    })
                except Exception as e:
                    abort(422)

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
            # check that user name or email is not used before
            elif User.query.filter_by(user_name=new_user_name):
                abort(404, 'User name is already used Please choose another one')
            elif User.query.filter_by(email=new_email):
                abort(404, 'E-Mail is already used Please choose another one or login')

            else:
                user = User_unconfirmed(user_name=new_user_name,
                                        email=new_email,
                                        role=new_role,
                                        password=set_password(new_password)
                                        )
                user.insert()

                return jsonify({
                    'success': True,
                    'message': 'User created successfully, Please wait for owner to confirm'
                })


        except Exception as e:
            abort(422)

    # get all users paginated endpoint.
    # permission: get_all_users
    @app.route('/users/<int:page>', methods=[ 'GET' ])
    def get_users(page):
        # check if user logged in and has permission

        if check_permissions(session['token'],'get_all_users',session['user_id']):
            if page:
                users_query = User.query\
                    .with_entities(User.id, User.user_name, User.email, User.role)\
                    .paginate(page, results_per_page, False).items
                users = [ user.format() for user in users_query ]
                return users
            else:
                page = 1
                users_query = User.query\
                    .with_entities(User.id, User.user_name, User.email, User.role)\
                    .paginate(page,results_per_page,False).items
                users = [ user.format() for user in users_query ]
                return users

        else:
            abort(401)


    # user log-in endpoint.
    # this endpoint should update session with user id and token if login is verified
    @app.route('/login', methods=[ 'GET' ])
    def user_login():
        pass

    # get all lists paginated endpoint.
    # permission: get_all_lists
    @app.route('/lists/<int:page>', methods=[ 'GET' ])
    def get_lists_paginated(page):
        pass

    # get list by id with cards in it paginated endpoint.
    # this endpoint should take list id and page number
    # permission: get_list
    @app.route('/list', methods=[ 'GET' ])
    def get_list():
        pass

    # create list endpoint.
    # this end point should take title, creator_id
    # permission: create_list
    @app.route('/list', methods=[ 'POST' ])
    def create_list():
        pass

    # update list by id endpoint.
    # this endpoint should take list id and title
    # permission: update_list
    @app.route('/list', methods=[ 'PATCH' ])
    def update_list():
        pass

    # delete list endpoint.
    # permission: delete_list
    @app.route('/list/<int:list_id>', methods=[ 'DELETE' ])
    def delete_list(list_id):
        pass

    # assign member to list by user id and list id endpoint.
    #this endpoint should take list_id and user_id
    # permission: assign_member_list
    @app.route('/assignation', methods=[ 'POST' ])
    def assign_member():
        pass

    # unassign member to list by user id and list id endpoint.
    # this endpoint should take list_id and user_id
    # permission: revoke_member_list
    @app.route('/revocation', methods=[ 'DELETE' ])
    def revoke_member():
        pass

    # get all cards ordered by comments count descending and paginated endpoint.
    # permission: get_card
    @app.route('/cards/<int:page>', methods=[ 'GET' ])
    def get_cards(page):
        pass

    # get card by id with first three comments endpoint.
    # permission: get_card
    @app.route('/card/<int:card_id>', methods=[ 'GET' ])
    def get_card(card_id):
        pass

    # create card endpoint.
    #this endpoint should take title, description, comments_count=0, list_id, creator_id
    # permission: create_card
    @app.route('/card', methods=[ 'POST' ])
    def create_card():
        pass

    # update card by card id endpoint.
    # this end point should take card id and at least one of title or description
    # permission: update_card
    @app.route('/card/', methods=[ 'PATCH' ])
    def update_card():
        pass

    # delete card by card id endpoint.
    # permission: delete_card
    @app.route('/card/<int:card_id>', methods=[ 'DELETE' ])
    def delete_card(card_id):
        pass

    # get all comments on a card ordered by id and paginated endpoint.
    # this should receive card id and page number
    # permission: get_comment
    @app.route('/card/comments/', methods=[ 'GET' ])
    def get_card_comments():
        pass

    # get comment by id with all replies and replies paginated endpoint.
    # this should receive comment id and page number
    # permission: get_comment
    @app.route('/comment/replies', methods=[ 'GET' ])
    def get_comment_replies():
        pass

    # create comment on card with card id endpoint.
    # this endpoint should add 1 to comments_count in card table
    # this endpoint should take content, replies_count =0, card_id, creator_id
    # permission: create_comment
    @app.route('/comment', methods=[ 'POST' ])
    def create_comment():
        pass

    # update comment endpoint.
    # this endpoint should take id and content
    # permission: update_comment
    @app.route('/comment', methods=[ 'PATCH' ])
    def update_comment():
        pass

    # delete comment endpoint.
    # this endpoint should subtract 1 to comments_count in card table
    # permission: delete_comment
    @app.route('/comment/<int:comment_id>', methods=[ 'DELETE' ])
    def delete_comment():
        pass

    # create reply endpoint.
    # this endpoint should add 1 to replies_count in comments table
    # this endpoint should take content, comment_id and creator_id
    # permission: create_replies
    @app.route('/reply', methods=[ 'POST' ])
    def create_reply():
        pass

    # update reply endpoint.
    # this endpoint should take reply id and content
    # permission: update_replies
    @app.route('/reply', methods=[ 'PATCH' ])
    def update_reply():
        pass

    # delete reply endpoint.
    # this endpoint should subtract 1 to replies_count in comments table
    # permission: delete_replies
    @app.route('/reply/<int:reply_id>', methods=[ 'DELETE' ])
    def delete_reply():
        pass






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

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        handling authorization errors
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app
