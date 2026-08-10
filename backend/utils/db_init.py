"""
Database initialization script
"""
from models import db, Category


def init_database(app):
    """Initialize database with tables and seed data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed categories if empty
        if Category.query.count() == 0:
            categories = [
                Category(name='items', description='Game Items', icon='⚔️'),
                Category(name='accounts', description='Game Accounts', icon='👤'),
                Category(name='currency', description='In-Game Currency', icon='💰')
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print('✅ Database initialized with seed data')
        else:
            print('ℹ️  Database already initialized')


def seed_sample_products(app):
    """Seed sample products for testing"""
    from models import Product, User
    
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            admin = User(username='admin', email='admin@gamevault.com', role='seller')
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
        
        # Seed sample products if none exist
        if Product.query.count() == 0:
            categories = {cat.name: cat.id for cat in Category.query.all()}
            
            sample_products = [
                {
                    'title': 'Legendary Dragon Sword',
                    'description': 'Rare mythical weapon with +500 attack power',
                    'price': 49.99,
                    'category_id': categories['items'],
                    'badge': 'Featured',
                    'stock_quantity': 5
                },
                {
                    'title': 'Fortnite Level 100 Account',
                    'description': 'Full Season Pass with exclusive skins',
                    'price': 129.99,
                    'category_id': categories['accounts'],
                    'badge': 'Verified',
                    'stock_quantity': 2
                },
                {
                    'title': '10,000 V-Bucks',
                    'description': 'Instant delivery for Fortnite currency',
                    'price': 79.99,
                    'category_id': categories['currency'],
                    'badge': 'Hot',
                    'stock_quantity': 100
                },
                {
                    'title': 'Epic Gaming Skin Pack',
                    'description': '5 ultra-rare skins bundle',
                    'price': 89.99,
                    'category_id': categories['items'],
                    'badge': 'New',
                    'stock_quantity': 10
                },
                {
                    'title': 'Diamond League Account',
                    'description': 'LoL account with 50+ champions',
                    'price': 199.99,
                    'category_id': categories['accounts'],
                    'badge': 'Featured',
                    'stock_quantity': 3
                },
                {
                    'title': '1 Million Gold Coins',
                    'description': 'FIFA Ultimate Team currency',
                    'price': 149.99,
                    'category_id': categories['currency'],
                    'badge': 'Hot',
                    'stock_quantity': 50
                },
            ]
            
            for product_data in sample_products:
                product = Product(seller_id=admin.id, **product_data)
                db.session.add(product)
            
            db.session.commit()
            print('✅ Sample products added')
        else:
            print('ℹ️  Products already exist')
