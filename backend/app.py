"""
GameVault Backend API - Main Application
"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db

# Import blueprints
from api.auth import auth_bp
from api.products import products_bp
from api.orders import orders_bp
from api.cart import cart_bp
from api.reviews import reviews_bp
from api.categories import categories_bp
from api.sellers import sellers_bp


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(sellers_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'message': 'GameVault API is running'}), 200
    
    # API info endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'GameVault API',
            'version': '1.0.0',
            'description': 'Backend API for GameVault marketplace',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth/*',
                'products': '/api/products',
                'orders': '/api/orders',
                'cart': '/api/cart',
                'reviews': '/api/reviews',
                'categories': '/api/categories',
                'sellers': '/api/sellers'
            }
        }), 200
    
    return app


def init_db_command():
    """Initialize the database"""
    from utils.db_init import init_database, seed_sample_products
    
    app = create_app()
    
    print('🔄 Initializing database...')
    init_database(app)
    
    print('🔄 Seeding sample data...')
    seed_sample_products(app)
    
    print('✅ Database setup complete!')


if __name__ == '__main__':
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        init_db_command()
    else:
        # Run the application
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        port = int(os.getenv('PORT', 5000))
        
        print(f'🚀 Starting GameVault API on port {port}')
        print(f'📝 Environment: {os.getenv("FLASK_ENV", "development")}')
        print(f'🔗 API URL: http://localhost:{port}')
        print(f'💚 Health check: http://localhost:{port}/health')
        
        app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
