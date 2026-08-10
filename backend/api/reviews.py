"""
Reviews API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review, Product, User

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api')


@reviews_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """Get reviews for a product"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)
    
    pagination = Review.query.filter_by(product_id=product_id).order_by(
        Review.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    reviews = [review.to_dict() for review in pagination.items]
    
    return jsonify({
        'reviews': reviews,
        'total': pagination.total,
        'average_rating': product.average_rating(),
        'pages': pagination.pages,
        'current_page': page
    }), 200


@reviews_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(product_id):
    """Create a review for a product"""
    user_id = get_jwt_identity()
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    rating = data.get('rating')
    comment = data.get('comment', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Check if user already reviewed this product
    existing = Review.query.filter_by(product_id=product_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'You have already reviewed this product'}), 409
    
    # Create review
    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'message': 'Review created successfully',
        'review': review.to_dict()
    }), 201


@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review"""
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    if review.user_id != user_id:
        return jsonify({'error': 'Not authorized to update this review'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'rating' in data:
        rating = data['rating']
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        review.rating = rating
    
    if 'comment' in data:
        review.comment = data['comment'].strip()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Review updated successfully',
        'review': review.to_dict()
    }), 200


@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review"""
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    user = User.query.get(user_id)
    if review.user_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized to delete this review'}), 403
    
    db.session.delete(review)
    db.session.commit()
    
    return jsonify({'message': 'Review deleted successfully'}), 200
