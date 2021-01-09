# Irithm-Python-flask-API

## Project Description
This is a web application where clients can create lists, add cards to a certain list, comment on cards and reply to a comment.

## Getting Started

### Installing Dependencies

#### Python 3.7

Install the latest version of python for your platform.

#### Virtual Environment

working within a virtual environment keeps dependencies for the project separate and organized.

#### PIP Dependencies

Once we have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```

This will install all of the required packag
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/) is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)  is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. 
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)  is an extension that provides bcrypt hashing utilities for your application.

## Database Setup
With Postgres running, restore a database using the irithm.psql file provided. From the backend folder in terminal run:
```bash
psql irithm < irithm.psql
```
Or create your own database and change the database_name in src\models\models.py 

## Data Migration & Running the server

From within the `\src` directory first ensure you are working using your created virtual environment.
First import our app to flask, execute:
```bash
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=true
```
Then make data migration:
```bash
flask db init
flask db migrate
flask db upgrade
```
To run the server, execute:

```bash
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py`.

## Assumptions:
### Owner:
- the owner of the app should assign his info to the owner table in the database.
- the owner info contains user name, email, role which is by default owner, password which should be hashed by bcrypt.
- the owner should be also added as an admin to the users table.
- owner have the following tasks assigned:
  - get all unconfirmed registered users from unconfirmed users table.
  - confirm an unconfirmed user to be added to the users database and deleted from the unconfirmed users table.
  - delete an unconfirmed user which will be deleted from the unconfirmed users table.
  - change role of a confirmed user from member to admin or vice versa.
### Users:
- there are two types of users confirmed or un confirmed.
- there are two roles for users and each role has it's permissions as follows:
  - Admin:
    - List:
      - Can create lists.
	  - Can remove/update his own lists, 
	  - Can read all lists.
    - Card: 
      - Can Create Cards on any list.
	  - Can remove/update his own cards and any other card in his own lists.
	  - can read all cards.
    - Comments: 
	  - Can update/remove his own comments and any other comment on his own lists.
	  - Can create a comment anywhere, can read all comments.
    - Member: can assign/unassign members on his own lists.
  - Member:
    - List: 
      - can access only lists assigned to him.
	- Cards: 
      - Can create a card on his lists.
      - can read all cards on his lists.
      - can update/remove his own cards
    - Comments: 
      - can create comment on any card. 
      - can reply to comments in his lists.
      - can read all comments on his lists. 
      - can remove his own comments including other people’s replies on it. 
      - can update his comments/replies.
### Roles:
- as there are only two roles in this app an assumption is made to store it as a Boolean datatype in the database.
- if no role is selected the user will be assigned ass a member stored as False.
- if Admin role is assigned it will be stored True.
## How The APP Works?
- user sign up.
- owner confirm user.
- user log in.
- user id and a JWT token containing user permissions is stored in session.
- user can do CRUD actions according to the permissions granted to him.
## Test:
- run `src\unit_test\unit_test.py`
## API References

### Getting Started

##### Base URL: 
Currently hosted locally at http://127.0.0.1:5000/.

##### Authentication: 
Currently working on a custom coded Authentication located in `auth.py`.
There are two main functions:
- `get_permissions(user_id)`: takes the user id and return a JWT token containing all user granted permissions.
- `check_permissions(token, permission, entity_id)`: check if session token contains the requested permission for a certain entity return true or false.

```
please note that is always better to use a third party authentication like auth0 so the sign in and permissions process can be handeled the using RBAC for our app.
```
### Error Handling:

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error": 400,
    "message": "Bad Request!!!! Please make sure the data you entered is correct"
}
```
The API will return error types when requests fail, example:
```bash
400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method Not Allowed
```
### Endpoints
#### owner end points.

##### GET '/unconfirmed'

- Function:get all unconfirmed users
- Requested Arguments: None
- Returns an object with users

##### POST '/user/confirmation/<int:user_id>'

- Function: confirm user sign-up request
- Requested Arguments: user_id
- Returns an object with success, custom message

##### DELETE '/user/confirmation/<int:user_id>'

- Function: delete user sign-up request
- Requested Arguments: user_id
- Returns an object with success, custom message

##### PATCH '/user-role/<int:user_id>'

- Function: change user role from admin to member and vice versa
- Requested Arguments: user_id, role
- Returns an object with success, custom message

#### User end points:

##### POST '/register'

- Function: allow user to sign up and wait owner to confirm.
- Requested Arguments:user_name, email, role
- Returns an object with success, custom message

##### GET '/users/<int:page>'

- Function: get all confirmed users paginated.
- Requested Arguments:permission to get_all_users and page number
- Returns an object with users

# user log-in endpoint.
# this endpoint should update session with user id and token if login is verified
##### POST '/login'

- Function: make user user log-in & update session with user id and token if login is verified
- Requested Arguments: password and user_name or email
- Returns an object with success, custom message

##### GET '/lists/<int:page>'

- Function: get all lists paginated
- Requested Arguments: permission to get_all_lists,and page number
- Returns an object with lists

##### GET '/list'

- Function: get list by id with cards in it paginated
- Requested Arguments: permission to get_list,list id and page number
- Returns an object with list and cards

##### POST '/list'

- Function: create list
- Requested Arguments: permission to create_list, title and creator_id
- Returns an object with success and custom message

##### PATCH '/list'

- Function: update list by id
- Requested Arguments:permission to update_list, list id and title
- Returns an object with success and custom message

##### DELETE '/list/<int:list_id>'

- Function: delete a certain list by id
- Requested Arguments: permission to delete_list and list id
- Returns an object with success and custom message

##### POST '/assignation'

- Function: assign member to access a list
- Requested Arguments: permission to assign_member_list, list_id and user_id
- Returns an object with success and custom message

##### DELETE '/revocation'

- Function: unassign member from list
- Requested Arguments: permission to revoke_member_list, list_id and user_id
- Returns an object with success and custom message

##### GET '/cards/<int:page>'

- Function:get all cards ordered by comments count descending and paginated
- Requested Arguments: permission to get_card & page number
- Returns an object with cards

##### GET '/card/<int:card_id>'

- Function: get card by id with first three comments
- Requested Arguments: permission to get_card and card_id
- Returns an object with card and comments

##### POST '/card'

- Function: create a new card in a list
- Requested Arguments: permission to create_card,title, description, list_id and creator_id
- Returns an object with success and custom message

##### PATCH '/card'

- Function:update card by card id endpoint
_ Requested Arguments: permission to update_card, card id, title or description
- Returns an object with success and custom message

##### DELETE '/card/<int:card_id>'

Function: delete card by card id
Requested Arguments: permission to delete_card and card_id
Returns an object with success and custom message

##### GET '/card/comments/'

- Function: get all comments on a card ordered by id and paginated endpoint
- Requested Arguments: permission to get_comment, card id and page number
- Returns an object with 

##### GET '/comment/replies'

- Function: get comment by id with all replies and replies paginated
- Requested Arguments: permission to get_replies, comment id and page number.
- Returns an object with comment and replies

##### POST '/comment'

- Function: create comment on card with card id and increment comments_count in card table
- Requested Arguments: permission to create_comment, content, card_id and creator_id
- Returns an object with success and custom message

# update comment endpoint.
# this endpoint should take id and content
# permission: update_comment
@app.route('/comment', methods=[ 'PATCH' ])
##### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 

# delete comment endpoint.
# this endpoint should subtract 1 to comments_count in card table
# permission: delete_comment
@app.route('/comment/<int:comment_id>', methods=[ 'DELETE' ])
##### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 

# create reply endpoint.
# this endpoint should add 1 to replies_count in comments table
# this endpoint should take content, comment_id and creator_id
# permission: create_replies
@app.route('/reply', methods=[ 'POST' ])
##### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 

# update reply endpoint.
# this endpoint should take reply id and content
# permission: update_replies
@app.route('/reply', methods=[ 'PATCH' ])
##### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 

# delete reply endpoint.
# this endpoint should subtract 1 to replies_count in comments table
# permission: delete_replies
@app.route('/reply/<int:reply_id>', methods=[ 'DELETE' ])
##### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 

