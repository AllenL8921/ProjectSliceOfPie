from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# General Class
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # Changed from db._Column to db.Column


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    addOn = db.Column(db.String(255))
    calories = db.Column(db.Integer)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cartItem_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, user_id, cartItem_id, quantity=1):
        self.user_id = user_id
        self.cartItem_id = cartItem_id
        self.quantity = quantity

    def update_quantity(self, quantity):
        self.quantity += quantity
        db.session.commit()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()


# Only inherit UserMixin for User object
# Create Schema for object
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    invoice = db.relationship("Invoice")
