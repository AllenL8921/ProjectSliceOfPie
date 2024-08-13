from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db #not sure why relative import no work 
from .models import User, Item, Cart

# Create blueprint
views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("new_home.html", user=current_user)


#render menu
@views.route("/items")
def display_items():
    # Query items from the database
    items = (
        # Item.query.all()
        Item.query.with_entities(Item.id, Item.name, Item.price).all()
    )

    # Render the HTML template with the items
    return render_template("new_items.html", items=items, user=current_user)



#add item to cart button
@views.route("/add_to_cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    if current_user.is_authenticated:
        userId = current_user.id
        cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=userId).first()

        # Already Exists, increment item quantity
        if cart_item:
            cart_item.quantity += 1
        else:
            cart = Cart(user_id=userId, cartItem_id=item_id, quantity=1) #creates new cart connected to the user's id
            db.session.add(cart)

        db.session.commit()  # Commit changes to the database
    else:
        flash("You need to log in to add items to your cart", category="danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("views.cart"))


#remove item from cart button
@views.route("/remove_from_cart/<int:item_id>", methods=["POST"])
def rmv_from_cart(item_id):
    cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=current_user.id).first()

    if not cart_item:
        return redirect(url_for("auth.login")) #if for some reason bugged, reload cart

    cart_item.deleteFromDB()

    return redirect(url_for('views.cart')) # reload cart with update


@views.route("/increment_quantity/<int:item_id>", methods=["POST"])
def increment_quantity(item_id):
    user_id = current_user.id
    cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=user_id).first()

    if not cart_item:
        return redirect(url_for('views.cart'))
    
    cart_item.quantity += 1
    db.session.commit()

    return redirect(url_for('views.cart'))


@views.route("/decrement_quantity/<int:item_id>", methods=["POST"])
def decrement_quantity(item_id):
    user_id = current_user.id
    cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=user_id).first()

    if not cart_item:
        return redirect(url_for('views.cart'))
    
    if(cart_item.quantity==1):
        db.session.delete(cart_item)

    if(cart_item.quantity>0):
        cart_item.quantity -= 1

    db.session.commit()

    return redirect(url_for('views.cart'))


#intermediary between "/items" and "/checkout" MENU -> CART -> CHECKOUT. 
#Uses same logic as "/checkout"
@views.route("/cart")
def cart():
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        cart = []
        sub_total = 0
        for cart_item in cart_items:
            item = Item.query.get(cart_item.cartItem_id)
            if item:
                total_items_price = item.price * cart_item.quantity
                sub_total += total_items_price
                cart.append({"item_id": item.id, "item_name": item.name,"quantity": cart_item.quantity, "price": total_items_price})
    else:
        flash("You need to log in to add items to your cart", category="danger")
        return redirect(url_for("auth.login"))

    return render_template("cart.html", cart=cart, user=current_user, sub_total=sub_total)


#final price and payment is determined
@views.route("/checkout")
def checkout():
    # Fetch cart for the current user by filtering with id
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # Create a list of dictionaries containing item details and quantities
    cart = []
    for cart_item in cart_items:
        item = Item.query.get(cart_item.cartItem_id) #cart_item.cartItem_id simply refers to the id of the items in current user's cart
        if item:
            cart.append({"item_name": item.name, "quantity": cart_item.quantity})

    return render_template("checkout.html", cart=cart, user=current_user)



#NEW add item to cart
@views.route("/add_to_cart_STATIC/<int:item_id>", methods=["POST"])
def add_to_cart_STATIC(item_id):
    if current_user.is_authenticated:
        item = Item.query.filter_by(id=item_id).first()
        userId = current_user.id
        cart_item = Cart.query.filter_by(cartItem_id=item_id, user_id=userId).first()

        if cart_item:
            cart_item.quantity += 1
        else:
            match item_id:
                case 1:
                    if not item:
                        newItem = Item(id = 1,name='Classic Cheese', price=9.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=1, quantity=1)
                    db.session.add(cart)
                case 2:
                    if not item:
                        newItem = Item(id = 2,name='Tandoori Paneer', price=10.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=2, quantity=1)
                    db.session.add(cart)
                case 3:
                    if not item:
                        newItem = Item(id = 3,name='Veggie Supreme', price=9.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=3, quantity=1)
                    db.session.add(cart)
                case 4:
                    if not item:
                        newItem = Item(id = 4,name='Double Paneer Supreme', price=11.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=4, quantity=1)
                    db.session.add(cart)
                case 5:
                    if not item:
                        newItem = Item(id = 5,name='Buffalo wings', price=8.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=5, quantity=1)
                    db.session.add(cart)
                case 6:
                    if not item:
                        newItem = Item(id = 6,name='Mozzarella sticks', price=8.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=6, quantity=1)
                    db.session.add(cart)
                case 7:
                    if not item:
                        newItem = Item(id = 7,name='Pret’s chocolate and almond butter cookies', price=2.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=7, quantity=1)
                    db.session.add(cart)
                case 8:
                    if not item:
                        newItem = Item(id = 8,name='Vegan coconut and mango pavlova', price=8.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=8, quantity=1)
                    db.session.add(cart)
                case 9:
                    if not item:
                        newItem = Item(id = 9,name='Orange, fennel and pea shoot salad with walnuts', price=8.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=9, quantity=1)
                    db.session.add(cart)
                case 10:
                    if not item:
                        newItem = Item(id = 10,name='Heritage tomato salad', price=7.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=10, quantity=1)
                    db.session.add(cart)
                case 11:
                    if not item:
                        newItem = Item(id = 11,name='Orange, fennel and pea shoot salad with walnuts', price=8.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=11, quantity=1)
                    db.session.add(cart)
                case 12:
                    if not item:
                        newItem = Item(id = 12,name='Cola', price=1.99)
                        db.session.add(newItem)
                    cart = Cart(user_id=userId, cartItem_id=12, quantity=1)
                    db.session.add(cart)

        db.session.commit()  # Commit changes to the database
    else:
        flash("You need to log in to add items to your cart", category="danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("views.cart"))