// Sample product data
const products = [
    {
        id: 1,
        title: "Legendary Dragon Sword",
        description: "Rare mythical weapon with +500 attack power",
        price: "$49.99",
        category: "items",
        icon: "⚔️",
        seller: "ProGamer",
        rating: "★★★★★",
        badge: "Featured"
    },
    {
        id: 2,
        title: "Fortnite Level 100 Account",
        description: "Full Season Pass with exclusive skins",
        price: "$129.99",
        category: "accounts",
        icon: "👤",
        seller: "AccountKing",
        rating: "★★★★★",
        badge: "Verified"
    },
    {
        id: 3,
        title: "10,000 V-Bucks",
        description: "Instant delivery for Fortnite currency",
        price: "$79.99",
        category: "currency",
        icon: "💰",
        seller: "CurrencyHub",
        rating: "★★★★☆",
        badge: "Hot"
    },
    {
        id: 4,
        title: "Epic Gaming Skin Pack",
        description: "5 ultra-rare skins bundle",
        price: "$89.99",
        category: "items",
        icon: "🎨",
        seller: "SkinStore",
        rating: "★★★★★",
        badge: "New"
    },
    {
        id: 5,
        title: "Diamond League Account",
        description: "LoL account with 50+ champions",
        price: "$199.99",
        category: "accounts",
        icon: "💎",
        seller: "EliteAccounts",
        rating: "★★★★★",
        badge: "Featured"
    },
    {
        id: 6,
        title: "1 Million Gold Coins",
        description: "FIFA Ultimate Team currency",
        price: "$149.99",
        category: "currency",
        icon: "🪙",
        seller: "CoinMaster",
        rating: "★★★★☆",
        badge: "Hot"
    },
    {
        id: 7,
        title: "Minecraft Rare Blocks",
        description: "Stack of Ancient Debris",
        price: "$24.99",
        category: "items",
        icon: "🧱",
        seller: "MineCrafter",
        rating: "★★★★★",
        badge: "New"
    },
    {
        id: 8,
        title: "Valorant Radiant Account",
        description: "High-tier rank with premium skins",
        price: "$299.99",
        category: "accounts",
        icon: "🎯",
        seller: "RadiantPro",
        rating: "★★★★★",
        badge: "Featured"
    },
    {
        id: 9,
        title: "CS:GO Knife Skin",
        description: "Factory New Karambit Fade",
        price: "$399.99",
        category: "items",
        icon: "🔪",
        seller: "CSGOTrade",
        rating: "★★★★★",
        badge: "Exclusive"
    },
    {
        id: 10,
        title: "Roblox 5000 Robux",
        description: "Premium currency instant delivery",
        price: "$59.99",
        category: "currency",
        icon: "🎮",
        seller: "RobuxShop",
        rating: "★★★★☆",
        badge: "Hot"
    },
    {
        id: 11,
        title: "Apex Legends Heirloom",
        description: "Rare character heirloom set",
        price: "$179.99",
        category: "items",
        icon: "🏆",
        seller: "ApexElite",
        rating: "★★★★★",
        badge: "Rare"
    },
    {
        id: 12,
        title: "Genshin Impact Account",
        description: "5-star characters with constellations",
        price: "$249.99",
        category: "accounts",
        icon: "⭐",
        seller: "GenshinPro",
        rating: "★★★★★",
        badge: "Featured"
    }
];

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    renderProducts('all');
    initializeEventListeners();
    initializeScrollEffects();
});

// Render products based on filter
function renderProducts(filter) {
    const productGrid = document.getElementById('productGrid');
    const filteredProducts = filter === 'all' 
        ? products 
        : products.filter(p => p.category === filter);
    
    productGrid.innerHTML = '';
    
    filteredProducts.forEach(product => {
        const productCard = createProductCard(product);
        productGrid.appendChild(productCard);
    });
}

// Create product card element
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in-up';
    card.setAttribute('data-category', product.category);
    
    card.innerHTML = `
        <div class="product-image" style="background: var(--gradient-${Math.floor(Math.random() * 3) + 1})">
            <span>${product.icon}</span>
            <span class="product-badge">${product.badge}</span>
        </div>
        <div class="product-info">
            <h3 class="product-title">${product.title}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-meta">
                <span class="product-price">${product.price}</span>
                <span class="product-seller">
                    <span class="seller-rating">${product.rating}</span>
                </span>
            </div>
            <button class="product-action" onclick="showProductModal(${product.id})">
                View Details
            </button>
        </div>
    `;
    
    return card;
}

// Show product details modal
function showProductModal(productId) {
    const product = products.find(p => p.id === productId);
    const modal = document.getElementById('productModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <div class="modal-product">
            <div class="product-image" style="background: var(--gradient-1); height: 300px; margin-bottom: 2rem;">
                <span style="font-size: 6rem;">${product.icon}</span>
            </div>
            <h2 style="margin-bottom: 1rem;">${product.title}</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">${product.description}</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 2rem;">
                <div style="background: var(--darker-bg); padding: 1rem; border-radius: 8px;">
                    <div style="color: var(--text-muted); font-size: 0.875rem;">Price</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--accent-color);">${product.price}</div>
                </div>
                <div style="background: var(--darker-bg); padding: 1rem; border-radius: 8px;">
                    <div style="color: var(--text-muted); font-size: 0.875rem;">Seller</div>
                    <div style="font-weight: 600;">${product.seller}</div>
                </div>
                <div style="background: var(--darker-bg); padding: 1rem; border-radius: 8px;">
                    <div style="color: var(--text-muted); font-size: 0.875rem;">Rating</div>
                    <div style="color: var(--warning);">${product.rating}</div>
                </div>
                <div style="background: var(--darker-bg); padding: 1rem; border-radius: 8px;">
                    <div style="color: var(--text-muted); font-size: 0.875rem;">Category</div>
                    <div style="font-weight: 600; text-transform: capitalize;">${product.category}</div>
                </div>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <h3 style="margin-bottom: 1rem;">Product Features</h3>
                <ul style="color: var(--text-secondary); line-height: 2;">
                    <li>✓ Instant delivery after payment</li>
                    <li>✓ 100% secure transaction</li>
                    <li>✓ Money-back guarantee</li>
                    <li>✓ 24/7 customer support</li>
                    <li>✓ Verified seller</li>
                </ul>
            </div>
            
            <div style="display: flex; gap: 1rem;">
                <button class="btn-primary-large" style="flex: 1;" onclick="addToCart(${product.id})">
                    Add to Cart
                </button>
                <button class="btn-secondary-large" style="flex: 1;" onclick="buyNow(${product.id})">
                    Buy Now
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Add to cart function
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        alert(`Added "${product.title}" to your cart!`);
        closeModal();
    }
}

// Buy now function
function buyNow(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        alert(`Proceeding to checkout for "${product.title}"`);
        closeModal();
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('productModal');
    modal.style.display = 'none';
}

// Initialize event listeners
function initializeEventListeners() {
    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            renderProducts(this.getAttribute('data-filter'));
        });
    });
    
    // Category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
            
            setTimeout(() => {
                const filterBtn = document.querySelector(`.filter-btn[data-filter="${category}"]`);
                if (filterBtn) {
                    filterBtn.click();
                }
            }, 500);
        });
    });
    
    // Navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch(this.value);
        }
    });
    
    const searchBtn = document.querySelector('.search-btn');
    searchBtn.addEventListener('click', function() {
        performSearch(searchInput.value);
    });
    
    // Modal close
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    // Close modal on outside click
    window.addEventListener('click', function(e) {
        const modal = document.getElementById('productModal');
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
}

// Search functionality
function performSearch(query) {
    if (!query.trim()) {
        alert('Please enter a search term');
        return;
    }
    
    const results = products.filter(p => 
        p.title.toLowerCase().includes(query.toLowerCase()) ||
        p.description.toLowerCase().includes(query.toLowerCase()) ||
        p.category.toLowerCase().includes(query.toLowerCase())
    );
    
    if (results.length === 0) {
        alert(`No results found for "${query}"`);
        return;
    }
    
    document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
    
    setTimeout(() => {
        const productGrid = document.getElementById('productGrid');
        productGrid.innerHTML = '';
        results.forEach(product => {
            const productCard = createProductCard(product);
            productGrid.appendChild(productCard);
        });
        
        // Update filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
    }, 500);
}

// Initialize scroll effects
function initializeScrollEffects() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe elements for animation
    document.querySelectorAll('.category-card, .product-card, .protection-card, .tip-card, .step-card').forEach(el => {
        observer.observe(el);
    });
    
    // Navbar scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.8)';
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// Smooth scroll for all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading animation for images
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Handle form submissions (placeholder)
function handleContactForm(e) {
    e.preventDefault();
    alert('Thank you for contacting us! We will get back to you soon.');
    return false;
}

// Newsletter subscription (placeholder)
function subscribeNewsletter(email) {
    if (!email || !email.includes('@')) {
        alert('Please enter a valid email address');
        return;
    }
    alert('Thank you for subscribing to our newsletter!');
}

// Add to favorites (placeholder)
function addToFavorites(productId) {
    alert('Added to favorites!');
}

// Share product (placeholder)
function shareProduct(productId) {
    const product = products.find(p => p.id === productId);
    if (navigator.share) {
        navigator.share({
            title: product.title,
            text: product.description,
            url: window.location.href
        });
    } else {
        alert('Share this product: ' + product.title);
    }
}

// Currency formatter
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Time ago formatter
function timeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + " years ago";
    
    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + " months ago";
    
    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + " days ago";
    
    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + " hours ago";
    
    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + " minutes ago";
    
    return Math.floor(seconds) + " seconds ago";
}

// Console message
console.log('%c🎮 GameVault Marketplace', 'font-size: 24px; font-weight: bold; color: #667eea;');
console.log('%cWelcome to the premier gaming marketplace!', 'font-size: 14px; color: #94a3b8;');
