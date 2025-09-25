from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extension import db, login_manager

users_bp = Blueprint("users", __name__, url_prefix="/users")

# ------------------ MODELS ------------------
class User(db.Model, UserMixin):
    __tablename__ = "Users"
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Role = db.Column(db.String(20), nullable=False)  # Customer/Seller/Admin

    def get_id(self):
        return str(self.UserID)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form["email"]
        role = request.form["role"]
     
        new_user = User(Username=username, Password=password, Email=email, Role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful, please login!", "success")
        return redirect(url_for("users.login"))
   
    return render_template("users/register.html")

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = User.query.filter_by(Username=username).first()
        if user and check_password_hash(user.Password, password):
            login_user(user)
            return redirect(url_for("users.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("users/login.html")

@users_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("users/dashboard.html", user=current_user)

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("users.login"))

# ------------------ ADMIN ------------------
# Admin Dashboard (Main page)
@users_bp.route("/admin")
@login_required
def admin_dashboard():
    if current_user.Role != "Admin":
        flash("Access denied!", "danger")
        return redirect(url_for("users.dashboard"))

    return render_template("admin/dashboard.html")   # sirf buttons show karega


# Manage Users page
@users_bp.route("/admin/users")
@login_required
def admin_users():
    if current_user.Role != "Admin":
        flash("Access denied!", "danger")
        return redirect(url_for("users.dashboard"))

    users = User.query.all()
    return render_template("admin/admin_users.html", users=users)


# Manage Products page
@users_bp.route("/admin/products")
@login_required
def admin_products():
    if current_user.Role != "Admin":
        flash("Access denied!", "danger")
        return redirect(url_for("users.dashboard"))

    from routes.products.products import Product
    products = Product.query.all()
    return render_template("admin/admin_products.html", products=products)


# Manage Orders page
@users_bp.route("/admin/orders")
@login_required
def admin_orders():
    if current_user.Role != "Admin":
        flash("Access denied!", "danger")
        return redirect(url_for("users.dashboard"))

    from routes.orders.orders import Order
    orders = Order.query.all()
    return render_template("admin/admin_orders.html",orders=orders)
