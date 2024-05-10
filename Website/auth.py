from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Item, Cart
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create blueprint
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # Compare the entered password with the saved password to the corresponding email
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in successfully", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("Email does not exist.", category="error")

    # You can pass variables to the html templates
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    # When user is submitting the method is POST
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        isAdmin = request.form.get("is_admin")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        # Define errors
        elif len(email) < 4:
            flash("Email is not valid.", category="error")
        elif len(firstName) < 2:
            flash("First Name is too Short.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Passwords is too short.", category="error")
        else:
            new_user = User(
                email=email,
                firstName=firstName,
                password=generate_password_hash(password1, method="pbkdf2:sha256"),
                is_admin=(isAdmin == "on"),
            )

            # add user to database
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(new_user, remember=True)

            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    if current_user.is_authenticated:
        userId = current_user.id
        cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=userId).first()

        # Already Exists, increment item quantity
        if cart_item:
            cart_item.quantity += 1
        else:
            cart = Cart(user_id=userId, cartItem_id=item_id, quantity=1)
            db.session.add(cart)

        db.session.commit()  # Commit changes to the database
    else:
        flash("You need to log in to add items to your cart", category="danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("auth.display_items"))


@auth.route("/items")
def display_items():
    # Query items from the database
    items = (
        # Item.query.all()
        Item.query.with_entities(Item.id, Item.name, Item.price).all()
    )

    # Render the HTML template with the items
    return render_template("items.html", items=items, user=current_user)


@auth.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        itemName = request.form.get("itemName")
        itemPrice = request.form.get("itemPrice")

        item = Item.query.filter_by(name=itemName).first()

        if item:
            flash("Item already exists.", category="error")
        else:
            newItem = Item(name=itemName, price=itemPrice)

            db.session.add(newItem)
            db.session.commit()

            flash("Item added.", category="success")

    return render_template("admin.html", user=current_user)


@auth.route("/checkout")
def checkout():
    # Fetch cart items for the current user
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # Create a list of dictionaries containing item details and quantities
    cart = []
    for cart_item in cart_items:
        item = Item.query.get(cart_item.cartItem_id)
        if item:
            cart.append({"item_name": item.name, "quantity": cart_item.quantity})

    return render_template("checkout.html", cart=cart, user=current_user)
