from flask import Flask 
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports] 
from extension import db, login_manager
from routes.users.users import users_bp, User
from routes.products.products import products_bp
from routes.orders.orders import orders_bp
 
from routes.products.products import products_bp

# Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
#db = SQLAlchemy(app)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "users.login"

def load_user(user_id):
    return User.query.get(int(user_id))

# Import blueprints
from routes.users.users import users_bp
from routes.products.products import products_bp
from routes.orders.orders import orders_bp

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
