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
The API will return three error types when requests fail:
```bash
400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method Not Allowed
```
### Endpoints

### GET '/'

#### Function:
#### Requested Arguments:
#### Response body:
##### Returns an object with 