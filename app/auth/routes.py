from flask import render_template, redirect, url_for, flash, request, session, g
from app.auth import bp
from app.auth.forms import LoginForm, AdminLoginForm
from app.models import User, Admin
from app import db, login_manager
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
import pymysql
import uuid
from app.config import Config

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Konverter booking-nummer og efternavn til lowercase for case-insensitive sammenligning
        booking_number = form.booking_number.data.lower()
        last_name = form.last_name.data.lower()
        
        # Tjek først om brugeren allerede findes i vores lokale database
        user = User.query.filter(
            db.func.lower(User.booking_number) == booking_number,
            db.func.lower(User.last_name) == last_name
        ).first()
        
        if not user:
            # Prøv at finde brugeren i booking-databasen
            try:
                connection = pymysql.connect(
                    host=Config.BOOKING_DB_HOST,
                    user=Config.BOOKING_DB_USER,
                    password=Config.BOOKING_DB_PASSWORD,
                    database=Config.BOOKING_DB_NAME,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                
                with connection.cursor() as cursor:
                    # SQL-forespørgsel til at finde gæsten i booking-systemet
                    # Opdateret til at bruge den korrekte tabel og kolonner
                    sql = """
                    SELECT booking_id, efternavn, email 
                    FROM aktive_bookinger 
                    WHERE LOWER(booking_id) = %s AND LOWER(efternavn) = %s
                    """
                    cursor.execute(sql, (booking_number, last_name))
                    result = cursor.fetchone()
                    
                    if result:
                        # Opret brugeren i vores lokale database
                        user = User(
                            booking_number=result['booking_id'],
                            last_name=result['efternavn'],
                            email=result['email'] if result['email'] else ''
                        )
                        # Generer en tilfældig adgangskode (bruges ikke til login, men kræves af UserMixin)
                        user.set_password(str(uuid.uuid4()))
                        db.session.add(user)
                        db.session.commit()
            except Exception as e:
                flash(f'Kunne ikke forbinde til booking-databasen. Kontakt venligst receptionen.', 'danger')
                return render_template('auth/login.html', title='Log ind', form=form)
            finally:
                if 'connection' in locals() and connection:
                    connection.close()
        
        if user:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Ugyldigt booking-nummer eller efternavn. Prøv igen.', 'danger')
    
    return render_template('auth/login.html', title='Log ind', form=form)

@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin is None or not admin.check_password(form.password.data):
            flash('Ugyldigt brugernavn eller adgangskode', 'danger')
            return redirect(url_for('auth.admin_login'))
        
        # Opret en bruger med admin-rettigheder
        user = User.query.filter_by(booking_number=admin.username).first()
        if not user:
            user = User(
                booking_number=admin.username,
                last_name='Admin',
                is_admin=True
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    
    return render_template('auth/admin_login.html', title='Admin Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Opret standard admin-bruger hvis den ikke findes
@bp.before_app_first_request
def create_default_admin():
    admin = Admin.query.filter_by(username=Config.ADMIN_USERNAME).first()
    if not admin:
        admin = Admin(username=Config.ADMIN_USERNAME)
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
