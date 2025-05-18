from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
session = Session()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(user_id)
