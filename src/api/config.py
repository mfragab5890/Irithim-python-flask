import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:tafiTAFI@127.0.0.1:5432/'
SQLALCHEMY_TRACK_MODIFICATIONS = False





        'create_replies': all_user_view_comments,
        'update_replies': all_user_created_replies,
        'delete_replies': all_user_created_replies,
        'get_replies': all_user_view_comments,