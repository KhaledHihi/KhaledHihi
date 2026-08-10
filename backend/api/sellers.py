"""
Sellers API routes
"""
from flask import Blueprint, request, jsonify
from models import Product, User, Review
from sqlalchemy import func

sellers_bp = Blueprint('sellers', __name__, url_prefix='/api/sellers')


@sellers_bp.route('/<int:seller_id>', methods=['GET'])
def get_seller(seller_id):
    """Get seller profile"""
    seller = User.query.get(seller_id)
    
    if not seller or seller.role not in ['seller', 'admin']:
        return jsonify({'error': 'Seller not found'}), 404
    
    # Get seller stats
    total_products = Product.query.filter_by(seller_id=seller_id, is_active=True).count()
    
    # Calculate average rating from all products
    products = Product.query.filter_by(seller_id=seller_id).all()
    all_reviews = []
    for product in products:
        all_reviews.extend(product.reviews.all())
    
    avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else 0
    
    return jsonify({
        'id': seller.id,
        'username': seller.username,
        'role': seller.role,
        'member_since': seller.created_at.isoformat(),
        'total_products': total_products,
        'average_rating': round(avg_rating, 2),
        'total_reviews': len(all_reviews)
    }), 200


@sellers_bp.route('/<int:seller_id>/products', methods=['GET'])
def get_seller_products(seller_id):
    """Get seller's products"""
    seller = User.query.get(seller_id)
    
    if not seller or seller.role not in ['seller', 'admin']:
        return jsonify({'error': 'Seller not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    per_page = min(per_page, 100)
    
    pagination = Product.query.filter_by(
        seller_id=seller_id,
        is_active=True
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    products = [product.to_dict() for product in pagination.items]
    
    return jsonify({
        'products': products,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200
