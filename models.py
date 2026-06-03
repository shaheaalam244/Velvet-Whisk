from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------------- USER ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    carts = db.relationship('Cart', backref='user', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    custom_orders = db.relationship('CustomOrder', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ---------------- CAKE ----------------
class Cake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    flavour = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.String(20))
    description = db.Column(db.String(250))
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- CART ----------------
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cake_id = db.Column(db.Integer, db.ForeignKey('cake.id'))
    quantity = db.Column(db.Integer, default=1)
    cake = db.relationship('Cake', backref='cart_items')


# ---------------- WISHLIST ----------------
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cake_id = db.Column(db.Integer, db.ForeignKey('cake.id'))
    cake = db.relationship('Cake', backref='wishlist_items')


# ---------------- ORDER ----------------
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_amount = db.Column(db.Float)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pending")

    # ✅ Relationship to items
    order_items = db.relationship('OrderItem', backref='order', lazy=True)


# ---------------- ORDER ITEM ----------------
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    cake_id = db.Column(db.Integer, db.ForeignKey('cake.id'))
    quantity = db.Column(db.Integer, default=1)
    cake = db.relationship('Cake')


# ---------------- CUSTOM ORDER ----------------
class CustomOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(300))
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
