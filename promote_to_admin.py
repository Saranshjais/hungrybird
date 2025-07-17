from app import db
from app.models import User
from run import app

admin_email = "hungrybird733@gmail.com"

with app.app_context():
    user = User.query.filter_by(email=admin_email).first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"✅ {user.username} has been promoted to admin.")
    else:
        print(f"❌ No user found with email {admin_email}")
