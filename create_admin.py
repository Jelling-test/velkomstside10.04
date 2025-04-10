from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Tjek om admin-brugeren allerede findes
        admin = Admin.query.filter_by(username='admin').first()
        
        if admin:
            print("Opdaterer eksisterende admin-bruger...")
            admin.password_hash = generate_password_hash('password')
        else:
            print("Opretter ny admin-bruger...")
            admin = Admin(username='admin')
            admin.password_hash = generate_password_hash('password')
            db.session.add(admin)
        
        db.session.commit()
        print("Admin-bruger oprettet/opdateret med:")
        print("Brugernavn: admin")
        print("Adgangskode: password")

if __name__ == '__main__':
    create_admin_user()
