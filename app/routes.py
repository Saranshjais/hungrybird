from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import csv

from . import db
from .models import User

# Import AI recommendation function if available
try:
    from .ai_recommender import recommend_vendors
except ImportError:
    recommend_vendors = lambda: []

main = Blueprint('main', __name__)

@main.route('/')
def index():
    vendor_data = []
    with open('google_places_vendors.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vendor_data.append({
                'name': row['name'],
                'lat': float(row['latitude']),
                'lng': float(row['longitude']),
                'city': row.get('city', 'Unknown'),
                'rating': float(row.get('rating', 4.0)),
                'image': row.get('image', ''),
                'cuisine': row.get('cuisine', 'Street Food')
            })

    return render_template('index.html', vendor_json=json.dumps(vendor_data))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form.get('username', email.split('@')[0])
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to 'user'

        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, username=username, password=hashed, role=role)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        if role == 'vendor':
            return redirect(url_for('main.vendor_setup'))
        elif role == 'admin':
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('main.index'))

    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.dashboard'))
            elif user.role == 'vendor':
                return redirect(url_for('main.vendor_setup'))
            else:
                return redirect(url_for('main.index'))
        else:
            return "Invalid email or password."

    return render_template('login.html')

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'admin':
        return "Access Denied: Only admins can access the dashboard.", 403

    try:
        recommended = recommend_vendors()
    except Exception as e:
        print(f"Error in recommendation: {e}")
        recommended = []

    return render_template('dashboard.html', recommended=recommended)

@main.route('/vendor_setup', methods=['GET', 'POST'])
@login_required
def vendor_setup():
    if current_user.role != 'vendor':
        return redirect(url_for('main.index'))

    return render_template('vendor_setup.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.favorite_cuisine = request.form.get('favorite_cuisine')
        db.session.commit()
        return redirect(url_for('main.profile'))
    return render_template('profile.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# ✅ NEW: Hidden Gems Route
@main.route('/hidden-gems')
def hidden_gems():
    vendor_data = []

    with open('hidden_vendors.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter by 'hidden' tag (optional)
            if row.get('tag', '').lower() == 'hidden':
                vendor_data.append({
                    'name': row['name'],
                    'lat': float(row['latitude']),
                    'lng': float(row['longitude']),
                    'city': row.get('city', 'Unknown'),
                    'rating': float(row.get('rating', 4.0)),
                    'image': row.get('image', ''),
                    'cuisine': row.get('cuisine', 'Street Food')
                })

    return render_template('hidden_gems.html', vendor_json=json.dumps(vendor_data))
