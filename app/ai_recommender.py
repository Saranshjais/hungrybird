from .models import FoodVendor
from flask_login import current_user

def recommend_vendors():
    if current_user.is_authenticated and current_user.favorite_cuisine:
        return FoodVendor.query.filter_by(cuisine=current_user.favorite_cuisine).limit(5).all()
    return FoodVendor.query.limit(5).all()

