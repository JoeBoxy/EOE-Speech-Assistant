from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from flask_app.views.auth import bp as auth_bp
    from flask_app.views.club import bp as club_bp
    from flask_app.views.meeting import bp as meeting_bp
    from flask_app.views.vote import bp as vote_bp
    from flask_app.views.member import bp as member_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(club_bp, url_prefix='/api')
    app.register_blueprint(meeting_bp, url_prefix='/api')
    app.register_blueprint(vote_bp, url_prefix='/api')
    app.register_blueprint(member_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'service': 'EOE演讲线上助手 Backend'}
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
