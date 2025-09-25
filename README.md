E-Commerce Web Application

 Objective
 Flask-based E-Commerce Web Application where:
● Users can register/login.
● Customers can browse products and place orders.
● Sellers can add/update products.
● Admin can view/manage users, products, and orders.

three roles: customer,admin,seller

Data can be stored in either:
SQLite (Recommended) – using ecommerce.db

📂 Directory Structure
Ecommerce_app1/
│── app.py               # Main app file
│── extensions.py        # Database & login manager
│── requirements.txt     # Dependencies
│── ecommerce.db         # SQLite database
│
├── routes/
│   ├── users/users.py       # Customer/Seller/Admin routes
│   ├── products/products.py # Product routes
│   └── orders/orders.py     # Order routes
│
├── templates/
│   ├── users/
│   │   ├── register.html
│   │   ├── login.html
│   │   └── dashboard.html
│   ├── products/
│   │   └── products.html
│   ├── orders/
│   │   └── orders.html
│   └── admin/
│       ├── dashboard.html
│       ├── admin_user.html
│       ├── admin_product.html
│       └── admin_order.html
│
└── static/ 


SQLite (Recommended)


CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE,
    Password TEXT,
    Email TEXT,
    Role TEXT CHECK(Role IN ('Customer','Seller','Admin'))
);

CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Price REAL,
    Stock INTEGER,
    SellerID INTEGER,
    FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);

CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    OrderDate DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


How to Run

Clone project

git clone <repo-url>
cd Ecommerce_app1


Create Virtual Environment

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac


Install Dependencies

pip install -r requirements.txt


Initialize Database

from app import app
from extensions import db

with app.app_context():
    db.create_all()


Run Application

python app.py


Open browser: http://127.0.0.1:5000

🔑 Features per Role

Customer → Register/Login, Browse Products, Place Orders

Seller → Login, Add Products, Update Stock & Price

Admin → Manage Users, Manage Products, View All Orders
