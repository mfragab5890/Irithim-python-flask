import jwt
from .models.models import *


# get_permissions
def get_permissions(user_id):
    # check role
    user = User.query.get(user_id)
    role = user.role
    # If role is true then user is admin
    if role:

        # get all user created lists
        user_owned_lists_query = List.query.filter(List.creator_id == user_id).all()
        user_owned_lists = [ lst.id for lst in user_owned_lists_query ]

        # get all cards on user lists or cards he created
        user_lists_cards_query = Cards.query.filter(Cards.list_id.in_(user_owned_lists)).all()
        user_lists_cards = [ crd.id for crd in user_lists_cards_query ]
        all_user_cards_query = Cards.query.filter(Cards.creator_id == user_id).all()
        all_user_cards = [ crd.id for crd in all_user_cards_query ]
        all_user_cards += user_lists_cards

        # get all user created comments or comments in his cards or cards in own lists
        user_own_comments_query = Comments.query.filter(Comments.creator_id == user_id).all()
        user_own_comments = [ cmnt.id for cmnt in user_own_comments_query ]
        user_cards_comments_query = Comments.query.filter(Comments.card_id.in_(user_lists_cards)).all()
        user_cards_comments = [ cmnt.id for cmnt in user_cards_comments_query ]
        all_user_comments = user_own_comments + user_cards_comments

        # get all user created replies or replies in his cards or cards in own lists
        all_user_replies_query = Replies.query.filter(Replies.comment_id.in_(all_user_comments)).all()
        all_user_replies = [ rply.id for rply in all_user_replies_query ]

        print(all_user_cards[2])
        # create payload
        payload = {
            'user_id': user_id,
            'role': 'Admin',
            'permissions': {
                'get_all_lists': 'All',
                'create_list': 'All',
                'update_list': user_owned_lists,
                'delete_list': user_owned_lists,
                'get_list': 'All',
                'assign_member_list': user_owned_lists,
                'revoke_member_list': user_owned_lists,
                'get_all_users': 'All',
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
        secret = 'Irithm task is awesome'
        algo = "HS256"

        # encode a jwt
        encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
        return encoded_jwt

    # if role is False the user is a member
    else:
        # get all lists assigned to the user
        user_assigned_lists_query = UserLists.query.filter(UserLists.user_id == user_id).all()
        user_assigned_lists = [lst.id for lst in user_assigned_lists_query]
        # get all cards on user lists and cards he created in his assigned lists
        all_user_view_cards_query = Cards.query.filter(Cards.list_id.in_(user_assigned_lists)).all()
        all_user_view_cards = [crd.id for crd in all_user_view_cards_query]

        all_user_created_cards_query = Cards.query.filter(Cards.creator_id == user_id).all()
        all_user_created_cards = [crd.id for crd in all_user_created_cards_query]

        # get all user created comments and comments in his cards  in assigned lists
        all_user_view_comments_query = Comments.query.filter(Comments.card_id.in_(all_user_view_cards)).all()
        all_user_view_comments = [cmnt.id for cmnt in all_user_view_comments_query]

        all_user_created_comments_query = Comments.query.filter(Comments.creator_id == user_id).all()
        all_user_created_comments = [cmnt.id for cmnt in all_user_created_comments_query]

        # get all user created replies or replies in his cards or cards in own lists
        all_user_view_replies_query = Replies.filter(Replies.comment_id.in_(all_user_view_comments)).all()
        all_user_view_replies = [rply.id for rply in all_user_view_replies_query]

        all_user_created_replies_query = Replies.query.filter(Replies.creator_id == user_id).all()
        all_user_created_replies = [ rply.id for rply in all_user_created_replies_query ]

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
        secret = 'Irithm task is awesome'
        algo = "HS256"

        # encode a jwt
        encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
        return encoded_jwt


# check_permissions
def check_permissions(token, permission, entity_id):
    # Decode a JWT
    secret = 'Irithm task is awesome'
    algo = 'HS256'
    payload = jwt.decode(token, secret, algorithms=algo, verify=True)
    if 'permissions' in payload:
        if payload['permissions'][permission]:
            if str(entity_id) in payload['permissions'][permission]:
                return True
            elif payload['permissions'][permission] == 'All':
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
