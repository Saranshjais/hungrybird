from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Create a test user
test_user = User(
    username='testuser',
    email='test@hungrybird.com',
    password=generate_password_hash('password123')
)

db.session.add(test_user)
db.session.commit()
print("✅ Test user created successfully!")
