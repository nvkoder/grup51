from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Name of the view to redirect to for logins

# To avoid circular imports, import routes here
from app import routes

# User loader function
@login_manager.user_loader
def load_user(user_id):
    # Local import to avoid circular imports
    from app.models import User
    return User.query.get(int(user_id))

