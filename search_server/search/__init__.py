from flask import Flask
from search.views.search import search_bp
import search.model  # Import the model to access init_db

def create_app():
    app = Flask(__name__)

    # Load the configuration from config.py
    app.config.from_pyfile('config.py')  # Ensure this line is here

    # Register the Blueprint with the app
    app.register_blueprint(search_bp)

    # Initialize the database (creates tables if they don't exist)
    with app.app_context():  # Ensure this is wrapped in an app context
        search.model.init_db()

    # Register the teardown function for closing the database
    app.teardown_appcontext(search.model.close_db)

    return app
