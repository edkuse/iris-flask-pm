from flask import Flask, render_template
from flask_login import current_user
from .config import Config
from .extensions import db, login_manager, migrate, session
from .utils.rbac import can_user


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    
    # Register blueprints
    from .blueprints.admin import bp as admin_bp
    from .blueprints.api import bp as api_bp
    from .blueprints.auth import bp as auth_bp
    from .blueprints.dashboard import bp as dashboard_bp
    from .blueprints.epics import bp as epics_bp
    from .blueprints.kanban import bp as kanban_bp
    from .blueprints.meetings import bp as meetings_bp
    from .blueprints.product_ideas import bp as product_ideas_bp
    from .blueprints.sprints import bp as sprints_bp
    from .blueprints.tasks import bp as tasks_bp
    from .blueprints.timeline import bp as timeline_bp
    from .blueprints.user_stories import bp as user_stories_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(epics_bp)
    app.register_blueprint(kanban_bp)
    app.register_blueprint(meetings_bp)
    app.register_blueprint(product_ideas_bp)
    app.register_blueprint(sprints_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(timeline_bp)
    app.register_blueprint(user_stories_bp)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Create a global context processor to make current user available in all templates
    @app.context_processor
    def inject_user():
        return dict(user=current_user)
    
    @app.context_processor
    def inject_rbac_utilities():
        return {
            'can_user': can_user
        }
    
    return app
