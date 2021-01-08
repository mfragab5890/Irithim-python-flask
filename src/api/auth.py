import jwt


# get_permissions
def get_permissions(user_id):
    # check role
    user = User.query.get(user_id)
    role = user.role
    # If role is true then user is admin
    if role:

        # get all user created lists
        user_owned_lists = List.query.with_entities(List.id).filter(List.creator_id == user_id).all()

        # get all cards on user lists or cards he created
        all_user_cards = db.session.query(User) \
            .join(Cards) \
            .filter(Cards.list_id.in_(user_owned_lists) | Cards.creator_id == user_id) \
            .with_entities(Cards.id) \
            .all()

        # get all user created comments or comments in his cards or cards in own lists
        all_user_comments = db.session.query(User) \
            .join(Comments) \
            .filter(Comments.card_id.in_(all_user_cards) | Comments.creator_id == user_id) \
            .with_entities(Comments.id) \
            .all()

        # get all user created replies or replies in his cards or cards in own lists
        all_user_replies = db.session.query(User) \
            .join(Replies) \
            .filter(Replies.comment_id.in_(all_user_comments) | Replies.creator_id == user_id) \
            .with_entities(Replies.id) \
            .all()

        # create payload
        payload = {
            'user_id': user_id,
            'role': 'Admin',
            'permissions': {
                'get_all_lists': {user_id},
                'create_list': {user_id},
                'update_list': user_owned_lists,
                'delete_list': user_owned_lists,
                'get_list': 'All',
                'assign_member_list': user_owned_lists,
                'revoke_member_list': user_owned_lists,
                'get_all_users': {user_id},
                'create_card': 'All',
                'update_card': all_user_cards,
                'delete_card': all_user_cards,
                'get_card': 'All',
                'create_comment': 'All',
                'update_comment': all_user_comments,
                'delete_comment': all_user_comments,
                'get_comment': 'All',
                'create_replies': 'All',
                'update_replies': all_user_replies,
                'delete_replies': all_user_replies,
                'get_replies': 'All',

            }
        }
        secret = app.config[ 'SECRET_KEY' ]
        algo = "HS256"

        # encode a jwt
        encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
        return encoded_jwt

    # if role is False the user is a member
    else:
        # get all lists assigned to the user
        user_assigned_lists = UserLists.query.with_entities(UserLists.list_id).filter(UserLists.user_id == user_id).all()

        # get all cards on user lists and cards he created in his assigned lists
        all_user_view_cards = db.session.query(User) \
            .join(Cards) \
            .filter(Cards.list_id.in_(user_assigned_lists)) \
            .with_entities(Cards.id) \
            .all()

        all_user_created_cards = db.session.query(User) \
            .join(Cards) \
            .filter(Cards.list_id.in_(Cards.creator_id == user_id)) \
            .with_entities(Cards.id) \
            .all()
        # get all user created comments and comments in his cards  in assigned lists
        all_user_view_comments = db.session.query(User) \
            .join(Comments) \
            .filter(Comments.card_id.in_(all_user_view_cards)) \
            .with_entities(Comments.id) \
            .all()

        all_user_created_comments = db.session.query(User) \
            .join(Comments) \
            .filter(Comments.creator_id == user_id) \
            .with_entities(Comments.id) \
            .all()
        # get all user created replies or replies in his cards or cards in own lists
        all_user_view_replies = db.session.query(User) \
            .join(Replies) \
            .filter(Replies.comment_id.in_(all_user_view_comments)) \
            .with_entities(Replies.id) \
            .all()

        all_user_created_replies = db.session.query(User) \
            .join(Replies) \
            .filter(Replies.creator_id == user_id) \
            .with_entities(Replies.id) \
            .all()

        # create payload
        payload = {
            'user_id': user_id,
            'role': 'Member',
            'permissions': {
                'get_all_lists': False,
                'create_list': False,
                'update_list': False,
                'delete_list': False,
                'get_list': user_assigned_lists,
                'get_all_users': False,
                'assign_member_list': False,
                'revoke_member_list': False,
                'create_card': user_assigned_lists,
                'update_card': all_user_created_cards,
                'delete_card': all_user_created_cards,
                'get_card': user_assigned_lists,
                'create_comment': all_user_view_cards,
                'update_comment': all_user_created_comments,
                'delete_comment': all_user_created_comments,
                'get_comment': all_user_view_cards,
                'create_replies': all_user_view_comments,
                'update_replies': all_user_created_replies,
                'delete_replies': all_user_created_replies,
                'get_replies': all_user_view_comments,

            }
        }
        secret = app.config[ 'SECRET_KEY' ]
        algo = "HS256"

        # encode a jwt
        encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
        return encoded_jwt


# check_permissions
def check_permissions(token, permission, entity_id):
    # Decode a JWT
    secret = app.config[ 'SECRET_KEY' ]
    payload = jwt.decode(token, secret, verify=True)
    if permission in payload:
        if payload.permission:
            if payload.permission == 'All':
                return True
            elif entity_id in payload.permission:
                return True
            else:
                raise AuthError({
                    'code': 'invalid_id',
                    'description': 'Authorization to this entity is forbidden.'
                }, 401)
        else:
            raise AuthError({
                'code': 'permission_access_forbidden',
                'description': 'Access to this entity is forbidden.'
            }, 401)

    else:
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'Permission not granted.'
        }, 401)


# authorization error class
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
