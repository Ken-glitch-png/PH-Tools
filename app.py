import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from models import db, User, GeolocationSearch, LinkCheck, FileCheck, Subscription
from forms import LoginForm, RegistrationForm, GeolocationForm, LinkCheckForm, FileCheckForm, GCashPaymentForm
from datetime import datetime, timedelta
import validators
import requests
from datetime import datetime
import json

# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'default-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    
    return app, login_manager

app, login_manager = create_app()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/validate-phone', methods=['POST'])
def validate_phone():
    # Simplified mock response
    result = {
        'is_valid': True,
        'provider': 'Globe',
        'formatted_number': '+63 917 123 4567',
        'location': 'Philippines'
    }
    return jsonify(result)

@app.route('/check-email', methods=['POST'])
def check_email():
    # Simplified mock response
    result = {
        'is_phishing': False,
        'confidence': 10,
        'reasons': ['Simplified check only'],
        'suspicious_links': [],
        'suspicious_keywords': []
    }
    return jsonify(result)

@app.route('/geolocation', methods=['GET', 'POST'])
@login_required
def geolocation():
    # Check if user can use geolocation (subscription or trial)
    can_use, access_type = current_user.can_use_geolocation()
    
    form = GeolocationForm()
    if form.validate_on_submit():
        # If user doesn't have access, redirect to payment page
        if not can_use:
            flash('You need to subscribe to use the geolocation service.', 'warning')
            return redirect(url_for('payment'))
            
        ip_address = form.ip_address.data
        
        # If using trial, mark it as used
        if access_type == "trial":
            current_user.use_geolocation_trial()
            db.session.commit()
            flash('You are using your free trial for the Geolocation service. Future searches will require a subscription.', 'info')
        
        # Mock geolocation data for Baguio
        location = "Baguio City, Philippines"
        isp = "PLDT"
        
        # Additional IP information
        ip_type = "IPv4" if "." in ip_address else "IPv6"
        country_code = "PH"
        region = "Cordillera Administrative Region"
        city = "Baguio City"
        postal_code = "2600"
        latitude = 16.4023
        longitude = 120.5960
        timezone = "Asia/Manila"
        
        # Save search to database
        search = GeolocationSearch(
            ip_address=ip_address,
            location=location,
            isp=isp,
            user_id=current_user.id
        )
        db.session.add(search)
        db.session.commit()
        
        return render_template('geolocation.html', 
                              form=form, 
                              result={
                                  'ip_address': ip_address,
                                  'location': location,
                                  'isp': isp,
                                  'ip_type': ip_type,
                                  'country_code': country_code,
                                  'region': region,
                                  'city': city,
                                  'postal_code': postal_code,
                                  'latitude': latitude,
                                  'longitude': longitude,
                                  'timezone': timezone
                              },
                              has_subscription=(access_type == "subscription"),
                              trial_available=(access_type == "trial"),
                              trial_used=(access_type == "trial"))
    
    # Get user's recent searches
    recent_searches = GeolocationSearch.query.filter_by(user_id=current_user.id).order_by(GeolocationSearch.timestamp.desc()).limit(5).all()
    
    return render_template('geolocation.html', form=form, recent_searches=recent_searches, 
                          has_subscription=(access_type == "subscription"),
                          trial_available=(access_type == "trial"))

@app.route('/link-checker', methods=['GET', 'POST'])
@login_required
def link_checker():
    form = LinkCheckForm()
    if form.validate_on_submit():
        url = form.url.data
        
        # Basic URL validation
        is_valid_url = validators.url(url)
        if not is_valid_url:
            flash('Invalid URL format')
            return redirect(url_for('link_checker'))
        
        # Mock link check result
        is_safe = True
        risk_score = 10
        
        # Save check to database
        check = LinkCheck(
            url=url,
            is_safe=is_safe,
            risk_score=risk_score,
            user_id=current_user.id
        )
        db.session.add(check)
        db.session.commit()
        
        return render_template('link_checker.html', 
                              form=form, 
                              result={
                                  'url': url,
                                  'is_safe': is_safe,
                                  'risk_score': risk_score
                              })
    
    # Get user's recent checks
    recent_checks = LinkCheck.query.filter_by(user_id=current_user.id).order_by(LinkCheck.timestamp.desc()).limit(5).all()
    
    return render_template('link_checker.html', form=form, recent_checks=recent_checks)

@app.route('/file-checker', methods=['GET', 'POST'])
@login_required
def file_checker():
    form = FileCheckForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get file type
        file_type = filename.split('.')[-1] if '.' in filename else 'unknown'
        
        # Mock file scan result
        is_safe = True
        scan_result = "No threats detected"
        
        # Save check to database
        check = FileCheck(
            filename=filename,
            file_type=file_type,
            is_safe=is_safe,
            scan_result=scan_result,
            user_id=current_user.id
        )
        db.session.add(check)
        db.session.commit()
        
        # Delete the file after scanning
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return render_template('file_checker.html', 
                              form=form, 
                              result={
                                  'filename': filename,
                                  'file_type': file_type,
                                  'is_safe': is_safe,
                                  'scan_result': scan_result
                              })
    
    # Get user's recent checks
    recent_checks = FileCheck.query.filter_by(user_id=current_user.id).order_by(FileCheck.timestamp.desc()).limit(5).all()
    
    return render_template('file_checker.html', form=form, recent_checks=recent_checks)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form = GCashPaymentForm()
    if form.validate_on_submit():
        # Process payment verification
        days = int(form.subscription_duration.data)
        
        # Create new subscription
        subscription = Subscription(
            user_id=current_user.id,
            service_type='geolocation',
            payment_method='gcash',
            payment_reference=form.reference_number.data,
            amount=float(form.amount.data),
            purchase_date=datetime.utcnow(),
            expiry_date=datetime.utcnow() + timedelta(days=days),
            is_active=True,
            auto_renew=form.auto_renew.data,
            gcash_number=form.phone_number.data
        )
        db.session.add(subscription)
        db.session.commit()
        
        auto_renew_msg = " with auto-renewal enabled" if form.auto_renew.data else ""
        flash(f'Your payment has been verified! You now have access to the Geolocation service{auto_renew_msg}.', 'success')
        return redirect(url_for('geolocation'))
    
    # Get user's subscriptions
    subscriptions = []
    if current_user.is_authenticated:
        subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    
    return render_template('payment.html', form=form, subscriptions=subscriptions, now=datetime.utcnow())

@app.route('/test')
def test():
    return "Flask server is running correctly!"

if __name__ == '__main__':
    # Make sure to bind to 0.0.0.0 to allow external access
    app.run(debug=True, host='0.0.0.0')