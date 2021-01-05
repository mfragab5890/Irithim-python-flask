import os
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# Declare database name
database_name = "irithm"

# initiate db with no assignment
db = SQLAlchemy()


# function is used to bend our app with the database
def setup_db(app, database_name):
    app.config.from_pyfile('config.py')
    app.config[ 'SQLALCHEMY_DATABASE_URI' ] += database_name
    moment = Moment(app)
    db.app = app
    db.init_app(app)
    # create instance migrate for data migration
    migrate = Migrate(app, db, compare_type=True)


# Users table

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Boolean, nullable=False)
    lists = db.relationship('UserLists', backref='user_lists', lazy=True, cascade="all, delete-orphan")
    cards = db.relationship('Cards', backref='user_comments', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comments', backref='user_comments', lazy=True, cascade="all, delete-orphan")
    replies = db.relationship('Replies', backref='user_replies', lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_name, email, password, role):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }


# Lists table

class List(db.Model):
    __tablename__ = 'Lists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    users = db.relationship('UserLists', backref='list_users', lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, creator_id):
        self.title = title
        self.creator_id = creator_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'creator_id': self.creator_id,
        }


# User lists table

class UserLists(db.Model):
    __tablename__ = 'users_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('List.id'), nullable=False)

    def __init__(self, user_id, list_id):
        self.user_id = user_id
        self.list_id = list_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'list_id': self.list_id,
        }


# Cards table

class Cards(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    comments_count = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('List.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    comments = db.relationship('Comments', backref='card_comments', lazy=True, cascade="all, delete-orphan")


    def __init__(self, title, description, comments_count, list_id, creator_id):
        self.title = title
        self.description = description
        self.comments_count = comments_count
        self.list_id = list_id
        self.creator_id = creator_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'comments_count': self.comments_count,
            'list_id': self.list_id,
            'creator_id': self.creator_id
        }

# Comments table

class Comments(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    replies_count = db.Column(db.Integer, nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('Cards.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    replies = db.relationship('replies', backref='comment_replies', lazy=True, cascade="all, delete-orphan")


    def __init__(self, content, replies_count, card_id, creator_id):
        self.content = content
        self.replies_count = replies_count
        self.card_id = card_id
        self.creator_id = creator_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'content': self.title,
            'card_id': self.card_id,
            'replies_count': self.replies_count,
            'creator_id': self.creator_id
        }

# Replies table

class Replies(db.Model):
    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('Comments.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, content, comment_id, creator_id):
        self.content = content
        self.comment_id = comment_id
        self.creator_id = creator_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'content': self.content,
            'comment_id': self.comment_id,
            'creator_id': self.creator_id
        }