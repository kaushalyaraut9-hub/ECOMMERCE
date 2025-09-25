from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extension import db
#from simple_rest_api.app import update_item

products_bp = Blueprint("products", __name__, url_prefix="/products")

# ------------------ MODELS ------------------
class Product(db.Model):
    __tablename__ = "Products"
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Stock = db.Column(db.Integer, nullable=False)
    SellerID = db.Column(db.Integer, db.ForeignKey("Users.UserID"), nullable=False)

# ------------------ CUSTOMER ------------------
@products_bp.route("/")
@login_required
def browse_products():
    all_products = Product.query.all()
    return render_template("products/products.html", products=all_products)


@products_bp.route("/buy/<int:product_id>")
@login_required
def buy(product_id):
    if current_user.Role != "Customer":
        flash("Only customers can buy products", "danger")
        return redirect(url_for("users.dashboard"))

    product = Product.query.get_or_404(product_id)

    if product.Stock > 0:
        product.Stock -= 1
        db.session.commit()
        flash(f"You bought {product.Name} successfully!", "success")
    else:
        flash("Product out of stock!", "danger")

    return redirect(url_for("products.browse_products"))


# ------------------ SELLER ------------------
@products_bp.route("/myproducts")
@login_required
def my_products():
    if current_user.Role != "Seller":
        flash("Only sellers can access this page", "danger")
        return redirect(url_for("users.dashboard"))
    
    edit_id = request.args.get("edit_id", type=int) 
    products = Product.query.filter_by(SellerID=current_user.UserID).all()
    return render_template("products/products.html", products=products,update_id=edit_id)

@products_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.Role != "Seller":
        flash("Only sellers can add products", "danger")
        return redirect(url_for("users.dashboard"))

    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])

        new_product = Product(Name=name, Price=price, Stock=stock, SellerID=current_user.UserID)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("products.my_products"))

    return render_template("products/products.html")

@products_bp.route("/update/<int:product_id>", methods=["POST"])
@login_required
def update_product(product_id): 
    product = Product.query.get_or_404(product_id)
    if current_user.Role != "Seller" or product.SellerID != current_user.UserID:
        flash("Not authorized!", "danger")
        return redirect(url_for("users.dashboard"))

    if request.method == "POST":
        product.Name = request.form["name"]
        product.Price = float(request.form["price"])
        product.Stock = int(request.form["stock"])
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("products.my_products"))
    #products=Product.query.all()
    #return render_template("products/products.html",products=products) #update_id=edit_id)

@products_bp.route("/delete/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.Role != "Seller" or product.SellerID != current_user.UserID:
        flash("Not authorized!", "danger")
        return redirect(url_for("users.dashboard"))

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "info")
    return redirect(url_for("products.my_products"))
