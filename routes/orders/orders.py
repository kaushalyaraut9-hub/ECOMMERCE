from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extension import db
from datetime import datetime
from routes.products.products import Product

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

# ------------------ MODELS ------------------
class Order(db.Model):
    __tablename__ = "Orders"
    OrderID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey("Users.UserID"), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey("Products.ProductID"), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    OrderDate = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders", lazy=True)
    product = db.relationship("Product", backref="orders", lazy=True)
# ------------------ CUSTOMER ------------------
@orders_bp.route("/buy/<int:product_id>")
@login_required
def buy_product(product_id):
    if current_user.Role != "Customer":
        flash("Only customers can buy products", "danger")
        return redirect(url_for("users.dashboard"))

    product = Product.query.get_or_404(product_id)
    if product.Stock < 1:
        flash("Product out of stock!", "danger")
        return redirect(url_for("products.browse_products"))

    product.Stock -= 1
    new_order = Order(UserID=current_user.UserID, ProductID=product.ProductID, Quantity=1)
    db.session.add(new_order)
    db.session.commit()
    flash("Order placed successfully!", "success")
    return redirect(url_for("orders.my_orders"))

@orders_bp.route("/myorders")
@login_required
def my_orders():
    if current_user.Role != "Customer":
        flash("Only customers can view this page", "danger")
        return redirect(url_for("users.dashboard"))

    orders = Order.query.filter_by(UserID=current_user.UserID).all()
    return render_template("orders/orders.html", orders=orders)

# ------------------ SELLER ------------------
@orders_bp.route("/seller_orders")
@login_required
def seller_orders():
    if current_user.Role != "Seller":
        flash("Only sellers can view this page", "danger")
        return redirect(url_for("users.dashboard"))

    orders = (
        db.session.query(Order)
        .join(Product)
        .filter(Product.SellerID == current_user.UserID)
        .all()
    )
    return render_template("orders/orders.html", orders=orders)
