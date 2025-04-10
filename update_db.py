from app import create_app, db
from app.models import User, PromotionOrder
import sqlalchemy as sa

app = create_app()
with app.app_context():
    try:
        # Tilføj first_name-kolonnen til User-tabellen, hvis den ikke allerede findes
        with db.engine.connect() as conn:
            conn.execute(sa.text('ALTER TABLE user ADD COLUMN first_name VARCHAR(100)'))
            
            # Tilføj comment-kolonnen til PromotionOrder-tabellen, hvis den ikke allerede findes
            conn.execute(sa.text('ALTER TABLE promotion_order ADD COLUMN comment TEXT'))
            
            conn.commit()
        
        print("Database opdateret med nye kolonner!")
    except Exception as e:
        print(f"Fejl ved opdatering af database: {e}")
