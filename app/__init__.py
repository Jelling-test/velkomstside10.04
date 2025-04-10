from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from app.config import Config
import os
from datetime import datetime

# Initialisér extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisér extensions med app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # Sørg for at upload-mapper eksisterer
    os.makedirs(os.path.join(app.static_folder, 'uploads', 'menu'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads', 'bakery'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads', 'posters'), exist_ok=True)
    
    # Registrér blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Sprog-håndtering
    @app.before_request
    def before_request():
        # Sæt standardsprog til dansk, hvis intet er valgt
        if 'language' not in session:
            session['language'] = 'da'
        
        # Gem det aktuelle tidspunkt til templates
        if 'now' not in g:
            g.now = datetime.now()
    
    # Tilføj hjælpefunktioner til Jinja2-templates
    @app.context_processor
    def utility_processor():
        def get_text(obj, field, lang=None):
            if not lang:
                lang = session.get('language', 'da')
            return getattr(obj, f"{field}_{lang}", getattr(obj, f"{field}_da", ""))
        
        def _(text):
            # Simpel oversættelsesfunktion
            translations = {
                'da': {
                    'Forside': 'Forside',
                    'Café': 'Café',
                    'Rundstykker': 'Rundstykker',
                    'Aktiviteter': 'Aktiviteter',
                    'Tilbud': 'Tilbud',
                    'Sprog': 'Sprog',
                    'Log ind': 'Log ind',
                    'Log ud': 'Log ud',
                    'Admin': 'Admin',
                    'Kontakt': 'Kontakt',
                    'Åbningstider': 'Åbningstider',
                    'Reception': 'Reception',
                    'Mandag-Søndag': 'Mandag-Søndag',
                    'Links': 'Links',
                    'Alle rettigheder forbeholdes.': 'Alle rettigheder forbeholdes.',
                    'Der er ingen kommende arrangementer i øjeblikket.': 'Der er ingen kommende arrangementer i øjeblikket.'
                },
                'en': {
                    'Forside': 'Home',
                    'Café': 'Café',
                    'Rundstykker': 'Bakery',
                    'Aktiviteter': 'Activities',
                    'Tilbud': 'Offers',
                    'Sprog': 'Language',
                    'Log ind': 'Log in',
                    'Log ud': 'Log out',
                    'Admin': 'Admin',
                    'Kontakt': 'Contact',
                    'Åbningstider': 'Opening Hours',
                    'Reception': 'Reception',
                    'Mandag-Søndag': 'Monday-Sunday',
                    'Links': 'Links',
                    'Alle rettigheder forbeholdes.': 'All rights reserved.',
                    'Der er ingen kommende arrangementer i øjeblikket.': 'There are no upcoming events at the moment.'
                }
            }
            
            lang = session.get('language', 'da')
            if lang in translations and text in translations[lang]:
                return translations[lang][text]
            return text
        
        return dict(get_text=get_text, _=_, now=datetime.now())
    
    return app


# Importér models efter app for at undgå cirkulære imports
from app import models
