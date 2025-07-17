from app import create_app, db
from app.models import FoodVendor  # and other models if needed

app = create_app()
app.app_context().push()

db.drop_all()       # Drop all tables
db.create_all()     # Recreate based on updated models

print("✅ Tables dropped and recreated successfully.")
