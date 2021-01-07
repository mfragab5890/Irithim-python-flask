from flask import session
from flask_session import Session


# setup Sessions with app
def setup_session(app, db):
    # Session configuration
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config[ 'SESSION_SQLALCHEMY' ] = db
    sess = Session(app)

    @app.route('/set/<user_data>')
    def set_session(user_data):
        session[ 'user_data' ] = user_data
        return 'session OK!'

    @app.route('/get/')
    def get_session():
        return session.get('user_data')
