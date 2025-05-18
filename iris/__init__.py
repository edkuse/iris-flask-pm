from flask import Flask
from flask_login import current_user
from .config import Config
from .extensions import db, migrate, login_manager, session


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    
    # Register blueprints
    from .blueprints.dashboard import dashboard_bp
    from .blueprints.product_ideas import product_ideas_bp
    from .blueprints.epics import epics_bp
    from .blueprints.user_stories import user_stories_bp
    from .blueprints.tasks import bp as tasks_bp
    from .blueprints.kanban import kanban_bp
    from .blueprints.timeline import bp as timeline_bp
    from .blueprints.api import api_bp
    from .blueprints.auth import bp as auth_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_ideas_bp, url_prefix='/product-ideas')
    app.register_blueprint(epics_bp, url_prefix='/epics')
    app.register_blueprint(user_stories_bp, url_prefix='/user-stories')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(kanban_bp, url_prefix='/kanban')
    app.register_blueprint(timeline_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)
    
    # Create a global context processor to make current user available in all templates
    @app.context_processor
    def inject_user():
        return dict(user=current_user)
    
    return app
