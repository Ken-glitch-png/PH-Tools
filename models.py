from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    geolocation_trial_used = db.Column(db.Boolean, default=False)
    
    # Relationships
    geolocation_searches = db.relationship('GeolocationSearch', backref='user', lazy='dynamic')
    link_checks = db.relationship('LinkCheck', backref='user', lazy='dynamic')
    file_checks = db.relationship('FileCheck', backref='user', lazy='dynamic')
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_active_geolocation_subscription(self):
        """Check if user has an active geolocation subscription"""
        active_sub = Subscription.query.filter_by(
            user_id=self.id,
            service_type='geolocation',
            is_active=True
        ).first()
        return active_sub is not None and active_sub.expiry_date > datetime.utcnow()
    
    def can_use_geolocation(self):
        """Check if user can use geolocation (has subscription or trial available)"""
        # Check for active subscription first
        if self.has_active_geolocation_subscription():
            return True, "subscription"
        # Check if trial is still available
        if not self.geolocation_trial_used:
            return True, "trial"
        # No subscription and trial used
        return False, None
        
    def use_geolocation_trial(self):
        """Mark the geolocation trial as used"""
        if not self.geolocation_trial_used:
            self.geolocation_trial_used = True
            return True
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_type = db.Column(db.String(50))  # 'geolocation', 'link_checker', etc.
    payment_method = db.Column(db.String(50))  # 'gcash', etc.
    payment_reference = db.Column(db.String(100))  # Reference number from payment
    amount = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    auto_renew = db.Column(db.Boolean, default=False)
    gcash_number = db.Column(db.String(20), nullable=True)  # Store GCash number for auto-renewal
    last_renewal_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Subscription {self.service_type} for User {self.user_id}>'
        
    def renew(self):
        """Renew the subscription for the same duration as the original"""
        if self.auto_renew and self.is_active:
            duration = (self.expiry_date - self.purchase_date).days
            self.last_renewal_date = datetime.utcnow()
            self.expiry_date = datetime.utcnow() + timedelta(days=duration)
            return True
        return False

class GeolocationSearch(db.Model):
    __tablename__ = 'geolocation_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))  # IPv6 addresses can be up to 45 chars
    location = db.Column(db.String(255))
    isp = db.Column(db.String(100))  # Changed provider to ISP for IP addresses
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<GeolocationSearch {self.ip_address}>'

class LinkCheck(db.Model):
    __tablename__ = 'link_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048))
    is_safe = db.Column(db.Boolean)
    risk_score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<LinkCheck {self.url}>'

class FileCheck(db.Model):
    __tablename__ = 'file_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    file_type = db.Column(db.String(50))
    is_safe = db.Column(db.Boolean)
    scan_result = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<FileCheck {self.filename}>'