import os
import sys
from datetime import datetime, timedelta
from flask import Flask
from models import db, Subscription, User
from app import create_app

def process_auto_renewals():
    """
    Process all subscriptions that are set to auto-renew and are about to expire
    This script should be run daily via a scheduler (cron job, Windows Task Scheduler, etc.)
    """
    app = create_app()
    with app.app_context():
        # Find subscriptions that are set to auto-renew and expire within the next 24 hours
        tomorrow = datetime.utcnow() + timedelta(days=1)
        expiring_subscriptions = Subscription.query.filter(
            Subscription.auto_renew == True,
            Subscription.is_active == True,
            Subscription.expiry_date <= tomorrow
        ).all()
        
        print(f"Found {len(expiring_subscriptions)} subscriptions to auto-renew")
        
        for subscription in expiring_subscriptions:
            # In a real system, you would process the GCash payment here
            # For this demo, we'll just renew the subscription
            if subscription.renew():
                print(f"Auto-renewed subscription {subscription.id} for user {subscription.user_id}")
                db.session.commit()
            else:
                print(f"Failed to auto-renew subscription {subscription.id}")

if __name__ == "__main__":
    process_auto_renewals()