"""
Products API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product, User, Category
from sqlalchemy import or_

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Limit per_page
    per_page = min(per_page, 100)
    
    # Build query
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                Product.title.like(search_term),
                Product.description.like(search_term)
            )
        )
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    products = [product.to_dict(include_seller=True) for product in pagination.items]
    
    return jsonify({
        'products': products,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    product = Product.query.get(product_id)
    
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict(include_seller=True)), 200


@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product (seller only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role not in ['seller', 'admin']:
        return jsonify({'error': 'Only sellers can create products'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    required_fields = ['title', 'description', 'price', 'category_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate category
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Invalid category'}), 400
    
    # Create product
    product = Product(
        seller_id=user_id,
        category_id=data['category_id'],
        title=data['title'],
        description=data['description'],
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 1),
        image_url=data.get('image_url'),
        badge=data.get('badge')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': product.to_dict(include_seller=True)
    }), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product (seller only)"""
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    user = User.query.get(user_id)
    if product.seller_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized to update this product'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update allowed fields
    if 'title' in data:
        product.title = data['title']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock_quantity' in data:
        product.stock_quantity = data['stock_quantity']
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'badge' in data:
        product.badge = data['badge']
    if 'is_active' in data:
        product.is_active = data['is_active']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if category:
            product.category_id = data['category_id']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product.to_dict(include_seller=True)
    }), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete product (seller only)"""
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    user = User.query.get(user_id)
    if product.seller_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized to delete this product'}), 403
    
    # Soft delete
    product.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200
