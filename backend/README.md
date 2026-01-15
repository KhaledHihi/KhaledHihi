# GameVault Backend API

Flask-based REST API for the GameVault marketplace with MariaDB database.

## Tech Stack

- **Backend Framework**: Flask (Python 3.9+)
- **Database**: MariaDB 10.6+
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Flask-RESTX (Swagger)
- **Security**: Flask-CORS, werkzeug password hashing

## Setup

### Prerequisites

- Python 3.9 or higher
- MariaDB 10.6 or higher
- pip package manager

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database:
```bash
# Create database
mysql -u root -p
CREATE DATABASE gamevault;
CREATE USER 'gamevault_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gamevault.* TO 'gamevault_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Set environment variables:
```bash
export DATABASE_URL="mysql+pymysql://gamevault_user:your_password@localhost/gamevault"
export SECRET_KEY="your-secret-key-here"
export JWT_SECRET_KEY="your-jwt-secret-key-here"
```

Or create a `.env` file:
```
DATABASE_URL=mysql+pymysql://gamevault_user:your_password@localhost/gamevault
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

4. Initialize database:
```bash
cd backend
python app.py init-db
```

5. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Once the server is running, visit `http://localhost:5000/docs` for interactive API documentation.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get user profile

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Create product (seller only)
- `PUT /api/products/<id>` - Update product (seller only)
- `DELETE /api/products/<id>` - Delete product (seller only)

### Categories
- `GET /api/categories` - List all categories

### Orders
- `GET /api/orders` - List user orders
- `GET /api/orders/<id>` - Get order details
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>/status` - Update order status

### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/<id>` - Update cart item
- `DELETE /api/cart/items/<id>` - Remove from cart

### Reviews
- `GET /api/products/<id>/reviews` - Get product reviews
- `POST /api/products/<id>/reviews` - Add review
- `PUT /api/reviews/<id>` - Update review
- `DELETE /api/reviews/<id>` - Delete review

### Sellers
- `GET /api/sellers/<id>` - Get seller profile
- `GET /api/sellers/<id>/products` - Get seller products
- `GET /api/sellers/<id>/ratings` - Get seller ratings

## Database Schema

### Users Table
- id (PK)
- username
- email
- password_hash
- role (buyer/seller/admin)
- created_at
- updated_at

### Products Table
- id (PK)
- seller_id (FK)
- category_id (FK)
- title
- description
- price
- stock_quantity
- image_url
- is_active
- created_at
- updated_at

### Categories Table
- id (PK)
- name
- description
- icon

### Orders Table
- id (PK)
- buyer_id (FK)
- total_amount
- status (pending/processing/completed/cancelled)
- created_at
- updated_at

### Order Items Table
- id (PK)
- order_id (FK)
- product_id (FK)
- quantity
- price
- subtotal

### Reviews Table
- id (PK)
- product_id (FK)
- user_id (FK)
- rating
- comment
- created_at

### Cart Table
- id (PK)
- user_id (FK)
- created_at

### Cart Items Table
- id (PK)
- cart_id (FK)
- product_id (FK)
- quantity

## Security Features

- Password hashing with werkzeug
- JWT token-based authentication
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Input validation
- Rate limiting

## Testing

Run tests:
```bash
python -m pytest tests/
```

## License

MIT License
