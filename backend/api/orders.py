"""
Orders API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, Product, Cart, User
from decimal import Decimal

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user orders"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    per_page = min(per_page, 100)
    
    pagination = Order.query.filter_by(buyer_id=user_id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    orders = [order.to_dict(include_items=True) for order in pagination.items]
    
    return jsonify({
        'orders': orders,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get single order"""
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    user = User.query.get(user_id)
    if order.buyer_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized to view this order'}), 403
    
    return jsonify(order.to_dict(include_items=True)), 200


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create order from cart"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    cart_items = user.cart.items.all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total and validate stock
    total_amount = Decimal('0.00')
    order_items_data = []
    
    for cart_item in cart_items:
        product = cart_item.product
        
        if not product or not product.is_active:
            return jsonify({'error': f'Product {product.title if product else "unknown"} is no longer available'}), 400
        
        if product.stock_quantity < cart_item.quantity:
            return jsonify({'error': f'Insufficient stock for {product.title}'}), 400
        
        subtotal = product.price * cart_item.quantity
        total_amount += subtotal
        
        order_items_data.append({
            'product_id': product.id,
            'quantity': cart_item.quantity,
            'price': product.price,
            'subtotal': subtotal
        })
    
    # Create order
    order = Order(
        buyer_id=user_id,
        total_amount=total_amount,
        status='pending'
    )
    db.session.add(order)
    db.session.flush()
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price=item_data['price'],
            subtotal=item_data['subtotal']
        )
        db.session.add(order_item)
        
        # Update product stock
        product = Product.query.get(item_data['product_id'])
        product.stock_quantity -= item_data['quantity']
    
    # Clear cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict(include_items=True)
    }), 201


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (seller/admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status required'}), 400
    
    new_status = data['status']
    valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
    
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    # Check authorization
    is_seller = any(item.product.seller_id == user_id for item in order.items.all())
    
    if not is_seller and user.role != 'admin':
        return jsonify({'error': 'Not authorized to update this order'}), 403
    
    order.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': 'Order status updated successfully',
        'order': order.to_dict(include_items=True)
    }), 200
