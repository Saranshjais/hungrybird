# models.py
from . import db
from flask_login import UserMixin

# 🔹 User Model for Login/Signup
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    favorite_cuisine = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20), default='user')


# 🔹 Food Vendor Model for Map/Dashboard
class FoodVendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cuisine = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(50))         # ✅ required
    rating = db.Column(db.Float, default=4.0)  # ✅ required
    image = db.Column(db.Text)
    categories=db.Column(db.String(200))
