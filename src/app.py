# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, request, jsonify, abort, session
from flask_cors import CORS
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

    # variable for pagination to show results per page
    results_per_page = 3

    # testing app
    @app.route('/', methods=[ 'GET' ])
    def index():
        session[ 'user_id' ] = 1
        session[
            'token' ] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiQWRtaW4iLCJwZXJtaXNzaW9ucyI6eyJnZXRfYWxsX2xpc3RzIjoiQWxsIiwiY3JlYXRlX2xpc3QiOiJBbGwiLCJ1cGRhdGVfbGlzdCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZGVsZXRlX2xpc3QiOlsxLDIsMyw0LDUsNiw3LDgsOSwxMF0sImdldF9saXN0IjoiQWxsIiwiYXNzaWduX21lbWJlcl9saXN0IjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJyZXZva2VfbWVtYmVyX2xpc3QiOlsxLDIsMyw0LDUsNiw3LDgsOSwxMF0sImdldF9hbGxfdXNlcnMiOiJBbGwiLCJjcmVhdGVfY2FyZCI6IkFsbCIsInVwZGF0ZV9jYXJkIjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfY2FyZCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X2NhcmQiOiJBbGwiLCJjcmVhdGVfY29tbWVudCI6IkFsbCIsInVwZGF0ZV9jb21tZW50IjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfY29tbWVudCI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X2NvbW1lbnQiOiJBbGwiLCJjcmVhdGVfcmVwbGllcyI6IkFsbCIsInVwZGF0ZV9yZXBsaWVzIjpbMSwyLDMsNCw1LDYsNyw4LDksMTBdLCJkZWxldGVfcmVwbGllcyI6WzEsMiwzLDQsNSw2LDcsOCw5LDEwXSwiZ2V0X3JlcGxpZXMiOiJBbGwifX0.SPGXta7MX1hDVmi2jOXR33pexRc7M9GJ9cWEZLGKQn8'
        owner = Owner.query.first()
        owner.role = 'owner'
        name = owner.user_name
        owner.update()
        query_user = User.query.get(1)
        user = query_user.format()
        query_lists = List.query.all()
        lists_ids = [ lst.id for lst in query_lists ]

        lists_query = db.session.query(Cards).join(List) \
            .filter(Cards.list_id == 1).order_by(db.desc(Cards.id)).all()
        user_list = [ lst.id for lst in lists_query ]
        user_list += lists_ids
        print(lists_query)
        return jsonify(user_list)

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
                return jsonify(users)
            else:
                abort(401)
        else:
            abort(401)

    # confirm users
    @app.route('/user/confirmation/<int:user_id>', methods=[ 'POST' ])
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
                    user.insert()
                    new_user.delete()
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
    @app.route('/user-role/<int:user_id>', methods=[ 'PATCH' ])
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
                        elif not role:
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

        new_user_name = body.get('user_name', None)
        new_email = body.get('email', None)
        new_role = body.get('role', False)
        if new_role:
            new_role = True
        new_password = body.get('password', None)
        try:
            if new_user_name is None or new_email is None or new_password is None:

                abort(400, 'data messing')
            # check that user name or email is not used before
            elif User.query.filter_by(user_name=new_user_name).first():
                abort(404, 'User name is already used Please choose another one')
            elif User.query.filter_by(email=new_email).first():
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
        token = 0
        logged_user_id = 0
        if 'token' in session:
            token = session[ 'token' ]
        elif 'token' in session:
            logged_user_id = session[ 'user_id' ]
        else:
            abort(401)
        if check_permissions(token, 'get_all_users', logged_user_id):
            if page:
                users_query = User.query.paginate(page, results_per_page, False).items
                users = [ user.format_no_password() for user in users_query ]
                return jsonify(users)
            else:
                page = 1
                users_query = User.query.paginate(page, results_per_page, False).items
                users = [ user.format_no_password() for user in users_query ]
                return jsonify(users)

        else:
            abort(401)

    # user log-in endpoint.
    # this endpoint should update session with user id and token if login is verified
    @app.route('/login', methods=[ 'POST' ])
    def user_login():
        body = request.get_json()
        user_name = body.get('user_name', None)
        email = body.get('email', None)
        password = body.get('password', None)
        if not password:
            abort(400, 'password not found')
        elif not email or not user_name:
            abort(400, 'email and user name not found')
        else:

            if email:
                user = User.query.filter_by(email=email).first()
            else:
                user = User.queryfilter_by(user_name=user_name).first()

            if check_password(user.password_hash, password):
                session[ 'user_id' ] = user.id
                session[ 'token' ] = get_permissions(user.id)

                return jsonify({
                    'success': True,
                    'message': 'logged in successfully'
                })

            else:
                abort(401, 'user name or password incorrect')

    # get all lists paginated endpoint.
    # permission: get_all_lists
    @app.route('/lists/<int:page>', methods=[ 'GET' ])
    def get_lists_paginated(page):
        if check_permissions(session[ 'token' ], 'get_all_lists', session[ 'user_id' ]):
            if page:
                lists_query = List.query.paginate(page, results_per_page, False).items
                lists = [ lst.format() for lst in lists_query ]
                return jsonify(lists)
            else:
                page = 1
                lists_query = List.query.paginate(page, results_per_page, False).items
                lists = [ lst.format() for lst in lists_query ]
                return jsonify(lists)
        else:
            abort(401)

    # get list by id with cards in it paginated endpoint.
    # this endpoint should take list id and page number
    # permission: get_list
    @app.route('/list', methods=[ 'GET' ])
    def get_list():
        body = request.get_json()
        list_id = body.get('list_id', None)
        page = body.get('page', None)
        if not list_id:
            abort(400)
        if check_permissions(session[ 'token' ], 'get_all_lists', list_id):
            if page:
                query_list = List.query.get(list_id)
                user_list = query_list.format()
                list_cards = db.session.query(Cards).join(List) \
                    .filter(List.id == list_id) \
                    .paginate(page, results_per_page, False).items
                cards = [ crd.format() for crd in list_cards ]
                return jsonify({
                    'list': user_list,
                    'cards': cards
                })
            else:
                query_list = List.query.get(list_id)
                user_list = query_list.format()
                list_cards = db.session.query(Cards).join(List) \
                    .filter(List.id == list_id) \
                    .paginate(page, results_per_page, False).items
                cards = [ crd.format() for crd in list_cards ]
                return jsonify({
                    'list': user_list,
                    'cards': cards
                })
        else:
            abort(401)

    # create list endpoint.
    # this end point should take title, creator_id
    # permission: create_list
    @app.route('/list', methods=[ 'POST' ])
    def create_list():
        body = request.get_json()

        new_title = body.get('title', None)
        new_creator_id = body.get('creator_id', None)
        try:
            if check_permissions(session[ 'token' ], 'create_list', session[ 'user_id' ]):
                if new_title is None or new_creator_id is None:
                    abort(400, 'data messing')
                else:
                    new_list = List(title=new_title, creator_id=new_creator_id)
                    new_list.insert()
                    # get new list id
                    user_list = List.query \
                        .filter(List.title == new_title, List.creator_id == new_creator_id) \
                        .order_by(db.desc(List.id)).first()
                    user_list_id = user_list.id
                    # assign user to list in users_lists table
                    user_id = session[ 'user_id' ]
                    new_user_list = UserLists(user_id=user_id, list_id=user_list_id)
                    new_user_list.insert()
                    return jsonify({
                        'success': True,
                        'message': 'list created successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # update list by id endpoint.
    # this endpoint should take list id and title
    # permission: update_list
    @app.route('/list', methods=[ 'PATCH' ])
    def update_list():
        body = request.get_json()

        new_title = body.get('title', None)
        list_id = body.get('list_id', None)
        try:
            if check_permissions(session[ 'token' ], 'update_list', list_id):
                if new_title is None or list_id is None:
                    abort(400, 'data messing')
                else:
                    user_list = List.query.get(list_id)
                    user_list.title = new_title
                    user_list.update()

                    return jsonify({
                        'success': True,
                        'message': 'list updated successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # delete list endpoint.
    # permission: delete_list
    @app.route('/list/<int:list_id>', methods=[ 'DELETE' ])
    def delete_list(list_id):
        try:
            if check_permissions(session[ 'token' ], 'delete_list', list_id):
                if list_id is None:
                    abort(400, 'data messing')
                else:
                    user_list = List.query.get(list_id)
                    user_list.delete()

                    return jsonify({
                        'success': True,
                        'message': 'list deleted successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # assign member to list by user id and list id endpoint.
    # this endpoint should take list_id and user_id
    # permission: assign_member_list
    @app.route('/assignation', methods=[ 'POST' ])
    def assign_member():
        body = request.get_json()

        user_list_id = body.get('list_id', None)
        user_id = body.get('user_id', None)
        try:
            if check_permissions(session[ 'token' ], 'assign_member_list', user_list_id):
                if user_id is None or user_list_id is None:
                    abort(400, 'data messing')
                else:
                    new_user_list = UserLists(user_id=user_id, list_id=user_list_id)
                    new_user_list.insert()

                    return jsonify({
                        'success': True,
                        'message': 'member assigned successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # unassign member to list by user id and list id endpoint.
    # this endpoint should take list_id and user_id
    # permission: revoke_member_list
    @app.route('/revocation', methods=[ 'DELETE' ])
    def revoke_member():
        body = request.get_json()

        user_list_id = body.get('list_id', None)
        user_id = body.get('user_id', None)
        try:
            if check_permissions(session[ 'token' ], 'revoke_member_list', user_list_id):
                if user_id is None or user_list_id is None:
                    abort(400, 'data messing')
                else:
                    user_list = UserLists.query.filter(UserLists.user_id == user_id, UserLists.list_id == user_list_id)
                    user_list.delete()

                    return jsonify({
                        'success': True,
                        'message': 'member revoked successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # get all cards ordered by comments count descending and paginated endpoint.
    # permission: get_card
    @app.route('/cards/<int:page>', methods=[ 'GET' ])
    def get_cards(page):
        if check_permissions(session[ 'token' ], 'get_card', session[ 'user_id' ]):
            if page:
                cards_query = Cards.query.order_by('comments_count').paginate(page, results_per_page, False).items
                cards = [ crd.format() for crd in cards_query ]
                return jsonify(cards)
            else:
                page = 1
                cards_query = Cards.query.order_by('comments_count').paginate(page, results_per_page, False).items
                cards = [ crd.format() for crd in cards_query ]
                return jsonify(cards)
        else:
            abort(401)

    # get card by id with first three comments endpoint.
    # permission: get_card
    @app.route('/card/<int:card_id>', methods=[ 'GET' ])
    def get_card(card_id):

        if check_permissions(session[ 'token' ], 'get_card', card_id):
            if card_id:
                cards_query = Cards.query.get(card_id)
                user_card = cards_query.format()
                comments_query = Comments.query.filter(Comments.card_id == card_id).limit(3).all()
                card_comments = [ cmnt.format() for cmnt in comments_query ]
                return jsonify({
                    'card': user_card,
                    'comments': card_comments
                })
            else:
                abort(400, 'data messing')
        else:
            abort(401)

    # create card endpoint.
    # this endpoint should take title, description, comments_count=0, list_id, creator_id
    # permission: create_card
    @app.route('/card', methods=[ 'POST' ])
    def create_card():
        body = request.get_json()

        new_title = body.get('title', None)
        new_description = body.get('description', None)
        new_comments_count = 0
        new_creator_id = body.get('creator_id', None)
        new_list_id = body.get('list_id', None)
        try:
            if check_permissions(session[ 'token' ], 'create_card', new_list_id):
                if new_title is None or new_creator_id is None or new_description is None or new_list_id is None:
                    abort(400, 'data messing')
                else:
                    new_card = Cards(
                        title=new_title,
                        description=new_description,
                        comments_count=new_comments_count,
                        creator_id=new_creator_id,
                        list_id=new_list_id,
                    )
                    new_card.insert()

                    return jsonify({
                        'success': True,
                        'message': 'card created successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # update card by card id endpoint.
    # this end point should take card id and at least one of title or description
    # permission: update_card
    @app.route('/card', methods=[ 'PATCH' ])
    def update_card():
        body = request.get_json()

        new_title = body.get('title', None)
        new_description = body.get('description', None)
        card_id = body.get('card_id', None)
        try:
            if check_permissions(session[ 'token' ], 'update_card', card_id):
                if new_title is None and new_description is None:
                    abort(400, 'data messing')
                else:
                    user_card = Cards.query.get(card_id)
                    if new_title:
                        user_card.title = new_title
                    elif new_description:
                        user_card.description = new_description
                    user_card.update()

                    return jsonify({
                        'success': True,
                        'message': 'card updated successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # delete card by card id endpoint.
    # permission: delete_card
    @app.route('/card/<int:card_id>', methods=[ 'DELETE' ])
    def delete_card(card_id):
        try:
            if not session[ 'token' ]:
                abort(401, 'please login first')
            if check_permissions(session[ 'token' ], 'delete_card', card_id):
                if card_id is None:
                    abort(400, 'data messing')
                else:
                    user_card = Cards.query.get(card_id)
                    user_card.delete()

                    return jsonify({
                        'success': True,
                        'message': 'card deleted successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # get all comments on a card ordered by id and paginated endpoint.
    # this should receive card id and page number
    # permission: get_comment
    @app.route('/card/comments/', methods=[ 'GET' ])
    def get_card_comments():
        body = request.get_json()

        user_card_id = body.get('card_id', None)
        page = body.get('page', None)
        if user_card_id is None:
            abort(400, 'data messing')
        if check_permissions(session[ 'token' ], 'get_comment', user_card_id):
            if page:
                comments_query = Comments.query.order_by('id').paginate(page, results_per_page, False).items
                comments = [ cmnt.format() for cmnt in comments_query ]
                return jsonify(comments)
            else:
                page = 1
                comments_query = Comments.query.order_by('id').paginate(page, results_per_page, False).items
                comments = [ cmnt.format() for cmnt in comments_query ]
                return jsonify(comments)
        else:
            abort(401)

    # get comment by id with all replies and replies paginated endpoint.
    # this should receive comment id and page number
    # permission: get_comment
    @app.route('/comment/replies', methods=[ 'GET' ])
    def get_comment_replies():
        body = request.get_json()

        user_comment_id = body.get('comment_id', None)
        page = body.get('page', None)
        if user_comment_id is None:
            abort(400, 'data messing')
        if check_permissions(session[ 'token' ], 'get_comment', user_comment_id):
            if page:
                comment_query = Comments.query.get(user_comment_id)
                user_comment = comment_query.format()
                replies_query = Replies.query.order_by('id').paginate(page, results_per_page, False).items
                comment_replies = [ reply.format() for reply in replies_query ]
                return jsonify({
                    'comment': user_comment,
                    'replies': comment_replies
                })
            else:
                page = 1
                comment_query = Comments.query.get(user_comment_id)
                user_comment = comment_query.format()
                replies_query = Replies.query.order_by('id').paginate(page, results_per_page, False).items
                comment_replies = [ reply.format() for reply in replies_query ]
                return jsonify({
                    'comment': user_comment,
                    'replies': comment_replies
                })
        else:
            abort(401)

    # create comment on card with card id endpoint.
    # this endpoint should add 1 to comments_count in card table
    # this endpoint should take content, replies_count =0, card_id, creator_id
    # permission: create_comment
    @app.route('/comment', methods=[ 'POST' ])
    def create_comment():
        body = request.get_json()

        new_content = body.get('content', None)
        new_card_id = body.get('card_id', None)
        new_replies_count = 0
        new_creator_id = body.get('creator_id', None)
        try:
            if check_permissions(session[ 'token' ], 'create_comment', new_card_id):
                if new_content is None or new_creator_id is None or new_card_id is None:
                    abort(400, 'data messing')
                else:
                    new_comment = Comments(
                        content=new_content,
                        replies_count=new_replies_count,
                        creator_id=new_creator_id,
                        card_id=new_card_id,
                    )
                    new_comment.insert()
                    # increment comments count on the card
                    user_card = Cards.query.get(new_card_id)
                    user_card.comments_count += 1
                    user_card.update()

                    return jsonify({
                        'success': True,
                        'message': 'comment created successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # update comment endpoint.
    # this endpoint should take id and content
    # permission: update_comment
    @app.route('/comment', methods=[ 'PATCH' ])
    def update_comment():
        body = request.get_json()

        new_content = body.get('content', None)
        comment_id = body.get('comment_id', None)
        try:
            if check_permissions(session[ 'token' ], 'update_comment', comment_id):
                if new_content is None or comment_id is None:
                    abort(400, 'data messing')
                else:
                    user_comment = Comments.query.get(comment_id)
                    if new_content:
                        user_comment.title = new_content
                    user_comment.update()

                    return jsonify({
                        'success': True,
                        'message': 'comment updated successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # delete comment endpoint.
    # this endpoint should subtract 1 to comments_count in card table
    # permission: delete_comment
    @app.route('/comment/<int:comment_id>', methods=[ 'DELETE' ])
    def delete_comment(comment_id):
        try:
            if not session[ 'token' ]:
                abort(401, 'please login first')
            if check_permissions(session[ 'token' ], 'delete_comment', comment_id):
                if comment_id is None:
                    abort(400, 'data messing')
                else:
                    user_comment = Comments.query.get(comment_id)
                    card_id = user_comment.card_id
                    user_comment.delete()
                    # decrement comments count on the card
                    user_card = Cards.query.get(card_id)
                    user_card.comments_count -= 1
                    user_card.update()
                    return jsonify({
                        'success': True,
                        'message': 'comment deleted successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # create reply endpoint.
    # this endpoint should add 1 to replies_count in comments table
    # this endpoint should take content, comment_id and creator_id
    # permission: create_replies
    @app.route('/reply', methods=[ 'POST' ])
    def create_reply():
        body = request.get_json()

        new_content = body.get('content', None)
        new_comment_id = body.get('comment_id', None)
        new_creator_id = body.get('creator_id', None)
        try:
            if check_permissions(session[ 'token' ], 'create_replies', new_comment_id):
                if new_content is None or new_creator_id is None or new_comment_id is None:
                    abort(400, 'data messing')
                else:
                    new_replies = Replies(
                        content=new_content,
                        creator_id=new_creator_id,
                        comment_id=new_comment_id,
                    )
                    new_replies.insert()
                    # increment repliess count on the card
                    user_card = Comments.query.get(new_comment_id)
                    user_card.replies_count += 1
                    user_card.update()

                    return jsonify({
                        'success': True,
                        'message': 'reply created successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # update reply endpoint.
    # this endpoint should take reply id and content
    # permission: update_replies
    @app.route('/reply', methods=[ 'PATCH' ])
    def update_reply():
        body = request.get_json()

        new_content = body.get('content', None)
        reply_id = body.get('reply_id', None)
        try:
            if check_permissions(session[ 'token' ], 'update_replies', reply_id):
                if new_content is None or reply_id is None:
                    abort(400, 'data messing')
                else:
                    user_reply = Replies.query.get(reply_id)
                    if new_content:
                        user_reply.title = new_content
                    user_reply.update()

                    return jsonify({
                        'success': True,
                        'message': 'reply updated successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

    # delete reply endpoint.
    # this endpoint should subtract 1 to replies_count in comments table
    # permission: delete_replies
    @app.route('/reply/<int:reply_id>', methods=[ 'DELETE' ])
    def delete_reply(reply_id):
        try:
            if not session[ 'token' ]:
                abort(401, 'please login first')
            if check_permissions(session[ 'token' ], 'delete_replies', reply_id):
                if reply_id is None:
                    abort(400, 'data messing')
                else:
                    user_reply = Replies.query.get(reply_id)
                    comment_id = user_reply.comment_id
                    user_reply.delete()
                    # decrement replies count on the card
                    user_comment = Comments.query.get(comment_id)
                    user_comment.replies_count -= 1
                    user_comment.update()
                    return jsonify({
                        'success': True,
                        'message': 'reply deleted successfully'
                    })
            else:
                abort(401)

        except Exception as e:
            abort(422)

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
