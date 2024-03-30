from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# General Class
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Changed from db._Column to db.Column


# Only inherit UserMixin for User object
# Create Schema for object
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)  # Changed from db._Column to db.Column
    password = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    invoice = db.relationship('Invoice')
