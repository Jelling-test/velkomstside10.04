import os
from datetime import timedelta

class Config:
    # Grundlæggende Flask-konfiguration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'en-meget-sikker-noegle-til-udvikling'
    
    # SQLAlchemy-konfiguration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload-konfiguration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    
    # Email-konfiguration
    MAIL_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('SMTP_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SMTP_USERNAME') or 'peter@jellingcamping.dk'
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD') or 'etde mpln hwia doxh'
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_FROM') or 'info@jellingcamping.dk'
    
    # Database-konfiguration for booking-systemet
    BOOKING_DB_HOST = os.environ.get('DB_HOST') or '192.168.1.254'
    BOOKING_DB_USER = os.environ.get('DB_USER') or 'windsurf'
    BOOKING_DB_PASSWORD = os.environ.get('DB_PASSWORD') or '7300Jelling!'
    BOOKING_DB_NAME = os.environ.get('DB_NAME') or 'camping_aktiv'
    
    # Bestillingstider for rundstykker
    BAKERY_ORDER_START_TIME = 10  # 10:00
    BAKERY_ORDER_END_TIME = 5     # 05:00
    BAKERY_PICKUP_START_TIME = 8  # 08:00
    BAKERY_PICKUP_END_TIME = 11   # 11:00
    
    # Admin-bruger (kan ændres via miljøvariabler)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'password'
    
    # Understøttede sprog
    LANGUAGES = ['da', 'en', 'de', 'nl', 'fi', 'no', 'sv']
