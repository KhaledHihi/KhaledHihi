"""
Cart API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Cart, CartItem, Product, User

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user cart"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.cart:
        # Create cart if not exists
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        return jsonify(cart.to_dict()), 200
    
    return jsonify(user.cart.to_dict()), 200


@cart_bp.route('/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    if quantity < 1:
        return jsonify({'error': 'Quantity must be at least 1'}), 400
    
    # Validate product
    product = Product.query.get(product_id)
    if not product or not product.is_active:
        return jsonify({'error': 'Product not found'}), 404
    
    if product.stock_quantity < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    # Get or create cart
    if not user.cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()
    else:
        cart = user.cart
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item.quantity + quantity
        if product.stock_quantity < new_quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        cart_item.quantity = new_quantity
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Item added to cart',
        'cart': cart.to_dict()
    }), 200


@cart_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """Update cart item quantity"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_item = CartItem.query.get(item_id)
    
    if not cart_item or cart_item.cart_id != user.cart.id:
        return jsonify({'error': 'Cart item not found'}), 404
    
    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Quantity required'}), 400
    
    quantity = data['quantity']
    
    if quantity < 1:
        return jsonify({'error': 'Quantity must be at least 1'}), 400
    
    if cart_item.product.stock_quantity < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({
        'message': 'Cart item updated',
        'cart': user.cart.to_dict()
    }), 200


@cart_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """Remove item from cart"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_item = CartItem.query.get(item_id)
    
    if not cart_item or cart_item.cart_id != user.cart.id:
        return jsonify({'error': 'Cart item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Item removed from cart',
        'cart': user.cart.to_dict()
    }), 200


@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    for item in user.cart.items.all():
        db.session.delete(item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Cart cleared',
        'cart': user.cart.to_dict()
    }), 200
