import csv
from app import create_app, db
from app.models import FoodVendor

# Initialize the app context
app = create_app()
app.app_context().push()

# Load vendor names from the CSV file
csv_file = 'more_famous_vendors.csv'
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    vendor_names = [row['name'].strip() for row in reader]

# Delete vendors whose names are in the CSV
deleted_count = FoodVendor.query.filter(FoodVendor.name.in_(vendor_names)).delete(synchronize_session=False)
db.session.commit()

print(f"✅ Deleted {deleted_count} vendors from database that matched CSV file.")
