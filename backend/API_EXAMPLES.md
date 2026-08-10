# GameVault API - Postman/cURL Examples

## Authentication

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "role": "buyer"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123"
  }'
```

### Get Profile (Requires JWT)
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Products

### Get All Products
```bash
curl -X GET "http://localhost:5000/api/products?page=1&per_page=12"
```

### Search Products
```bash
curl -X GET "http://localhost:5000/api/products?search=sword&category_id=1"
```

### Get Single Product
```bash
curl -X GET http://localhost:5000/api/products/1
```

### Create Product (Seller Only)
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Epic Battle Axe",
    "description": "Legendary weapon with massive damage",
    "price": 99.99,
    "category_id": 1,
    "stock_quantity": 5,
    "badge": "New"
  }'
```

### Update Product (Seller Only)
```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "price": 89.99,
    "stock_quantity": 10
  }'
```

### Delete Product (Seller Only)
```bash
curl -X DELETE http://localhost:5000/api/products/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Cart

### Get Cart
```bash
curl -X GET http://localhost:5000/api/cart \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Add to Cart
```bash
curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Update Cart Item
```bash
curl -X PUT http://localhost:5000/api/cart/items/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "quantity": 3
  }'
```

### Remove from Cart
```bash
curl -X DELETE http://localhost:5000/api/cart/items/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Clear Cart
```bash
curl -X DELETE http://localhost:5000/api/cart/clear \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Orders

### Get All Orders
```bash
curl -X GET http://localhost:5000/api/orders \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Single Order
```bash
curl -X GET http://localhost:5000/api/orders/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create Order from Cart
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update Order Status (Seller/Admin Only)
```bash
curl -X PUT http://localhost:5000/api/orders/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "status": "completed"
  }'
```

## Reviews

### Get Product Reviews
```bash
curl -X GET http://localhost:5000/api/products/1/reviews
```

### Create Review
```bash
curl -X POST http://localhost:5000/api/products/1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "rating": 5,
    "comment": "Excellent product! Fast delivery and great quality."
  }'
```

### Update Review
```bash
curl -X PUT http://localhost:5000/api/reviews/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "rating": 4,
    "comment": "Good product overall."
  }'
```

### Delete Review
```bash
curl -X DELETE http://localhost:5000/api/reviews/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Categories

### Get All Categories
```bash
curl -X GET http://localhost:5000/api/categories
```

### Get Single Category
```bash
curl -X GET http://localhost:5000/api/categories/1
```

## Sellers

### Get Seller Profile
```bash
curl -X GET http://localhost:5000/api/sellers/1
```

### Get Seller Products
```bash
curl -X GET http://localhost:5000/api/sellers/1/products
```

## Health Check

```bash
curl -X GET http://localhost:5000/health
```
