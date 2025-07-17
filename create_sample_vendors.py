from app import create_app, db
from app.models import FoodVendor

app = create_app()
app.app_context().push()

# Add sample vendors
vendors = [
    FoodVendor(name="Tandoori Tikka", latitude=26.9124, longitude=75.7873, cuisine="Indian", rating=4.6),
    FoodVendor(name="Urban Chaat", latitude=26.9130, longitude=75.7890, cuisine="Street Food", rating=4.3),
    FoodVendor(name="Noodle Hub", latitude=26.9112, longitude=75.7865, cuisine="Chinese", rating=4.1),
    FoodVendor(name="Vegan Delight", latitude=26.9100, longitude=75.7850, cuisine="Healthy", rating=4.8),
]

db.session.add_all(vendors)
db.session.commit()

print("✅ Sample food vendors inserted into database.")
