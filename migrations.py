from iris import create_app
from iris.extensions import db
from flask_migrate import upgrade, migrate, init, stamp
import os


def run_migrations():
    app = create_app()
    with app.app_context():
        # Initialize migrations if they don't exist
        if not os.path.exists('migrations'):
            init()
            stamp()
        
        # Generate migration
        migrate()
        
        # Apply migration
        upgrade()
        
        print("Migrations complete!")


if __name__ == "__main__":
    run_migrations()
    