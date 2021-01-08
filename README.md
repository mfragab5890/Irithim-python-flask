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

From within the `src\api` directory first ensure you are working using your created virtual environment.
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


