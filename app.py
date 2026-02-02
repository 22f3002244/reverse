from flask import Flask
from database import Base, engine
import os

# Import blueprints
from routes.auth import auth_bp
from routes.user import user_bp
from routes.lister import lister_bp
from routes.venue import venue_bp
from routes.events import events_bp
from routes.tickets import tickets_bp
from routes.bookings import bookings_bp
from routes.entry import entry_bp
from routes.general import general_bp

# Import models so SQLAlchemy registers them
from models import *

def create_app():
    app = Flask(__name__)
    
    # Set secret key for session management
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(lister_bp)
    app.register_blueprint(venue_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(entry_bp)
    app.register_blueprint(general_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
