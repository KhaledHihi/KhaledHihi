# GameVault - Complete Setup Guide

This guide will walk you through setting up both the frontend and backend of GameVault marketplace.

## Prerequisites

- **Python 3.9+** - For backend API
- **MariaDB 10.6+** - Database server
- **Modern web browser** - For frontend
- **Git** - Version control

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/KhaledHihi/KhaledHihi.git
cd KhaledHihi
```

### 2. Setup Backend

#### Install MariaDB

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mariadb-server mariadb-client
sudo mysql_secure_installation
```

**macOS (with Homebrew):**
```bash
brew install mariadb
brew services start mariadb
mysql_secure_installation
```

**Windows:**
Download and install from [MariaDB official website](https://mariadb.org/download/)

#### Create Database

```bash
# Login to MariaDB
mysql -u root -p

# Run the setup script
SOURCE backend/setup_database.sql;

# Or manually:
CREATE DATABASE gamevault CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gamevault_user'@'localhost' IDENTIFIED BY 'gamevault_pass';
GRANT ALL PRIVILEGES ON gamevault.* TO 'gamevault_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Setup Python Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and update with your settings
nano .env
```

Update these values in `.env`:
```
DATABASE_URL=mysql+pymysql://gamevault_user:YOUR_PASSWORD@localhost/gamevault
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
```

#### Initialize Database

```bash
# Create tables and seed sample data
python app.py init-db
```

#### Run Backend Server

```bash
# Start the API server
python app.py

# Server will run on http://localhost:5000
```

### 3. Setup Frontend

The frontend is ready to use - just open `index.html` in a web browser or serve it with a web server.

#### Option 1: Direct Browser Access

```bash
# Navigate to root directory
cd ..

# Open index.html in your default browser
# On Linux:
xdg-open index.html

# On macOS:
open index.html

# On Windows:
start index.html
```

#### Option 2: Python HTTP Server

```bash
# In the root directory (not backend)
python3 -m http.server 8000

# Visit http://localhost:8000
```

#### Option 3: Node.js http-server

```bash
# Install http-server globally
npm install -g http-server

# Serve the frontend
http-server -p 8000

# Visit http://localhost:8000
```

### 4. Connect Frontend to Backend

Update the API endpoint in `script.js`:

```javascript
// Find this line near the top of script.js
const API_BASE_URL = 'http://localhost:5000/api';
```

## Testing the Setup

### 1. Test Backend API

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test categories endpoint
curl http://localhost:5000/api/categories

# Test products endpoint
curl http://localhost:5000/api/products
```

### 2. Test Frontend

1. Open http://localhost:8000 in your browser
2. Browse products
3. Try search functionality
4. Filter by category
5. Click "View Details" on a product

### 3. Test Full Integration

#### Register a User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "role": "buyer"
  }'
```

#### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'
```

Save the `access_token` from the response for authenticated requests.

## Default Credentials

After running `python app.py init-db`, you can use these credentials:

- **Username:** admin
- **Password:** Admin@123
- **Role:** seller

## Project Structure

```
KhaledHihi/
├── backend/                  # Backend API
│   ├── api/                 # API route blueprints
│   │   ├── auth.py         # Authentication routes
│   │   ├── products.py     # Product management
│   │   ├── orders.py       # Order management
│   │   ├── cart.py         # Shopping cart
│   │   ├── reviews.py      # Product reviews
│   │   ├── categories.py   # Categories
│   │   └── sellers.py      # Seller profiles
│   ├── models.py           # Database models
│   ├── config.py           # Configuration
│   ├── app.py              # Main application
│   ├── requirements.txt    # Python dependencies
│   ├── utils/              # Utility functions
│   │   ├── validators.py   # Input validation
│   │   └── db_init.py      # Database initialization
│   ├── tests/              # Test files
│   └── README.md           # Backend documentation
├── index.html              # Frontend HTML
├── styles.css              # Frontend styles
├── script.js               # Frontend JavaScript
└── README.md               # This file
```

## API Documentation

Full API documentation with examples is available in:
- `backend/README.md` - API overview
- `backend/API_EXAMPLES.md` - cURL examples

## Troubleshooting

### Database Connection Error

If you get "Access denied" error:
```bash
# Reset MariaDB user password
mysql -u root -p
ALTER USER 'gamevault_user'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

Then update `DATABASE_URL` in `.env`

### Port Already in Use

If port 5000 is already in use:
```bash
# Change port in backend
export PORT=5001
python app.py
```

If port 8000 is already in use:
```bash
# Use different port for frontend
python3 -m http.server 8001
```

### CORS Issues

If you experience CORS errors, ensure:
1. Backend is running on `http://localhost:5000`
2. Frontend is accessing from same origin or CORS is properly configured
3. Check browser console for specific errors

### Import Errors

If you get module import errors:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Production Deployment

### Backend (Python API)

1. Update environment variables in `.env`:
   - Set `FLASK_ENV=production`
   - Use strong SECRET_KEY and JWT_SECRET_KEY
   - Update DATABASE_URL with production credentials

2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Setup reverse proxy (Nginx/Apache)
4. Enable HTTPS with SSL certificate

### Frontend

1. Update API_BASE_URL in `script.js` to production API URL
2. Host on static site hosting:
   - Netlify
   - Vercel
   - GitHub Pages
   - AWS S3 + CloudFront
   - Any web server (Apache/Nginx)

### Database

1. Backup regularly
2. Use connection pooling
3. Enable SSL for database connections
4. Implement database replication for high availability

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database backups
- [ ] Rate limiting on API endpoints
- [ ] Input validation and sanitization
- [ ] SQL injection prevention (using ORM)
- [ ] XSS protection

## Support

For issues or questions:
- Check existing documentation
- Review API examples
- Check server logs
- Test with cURL commands

## License

MIT License
