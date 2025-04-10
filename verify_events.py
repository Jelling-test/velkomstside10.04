from app import app, db
from app.models import Event
from datetime import datetime

def verify_events():
    with app.app_context():
        events = Event.query.all()
        print(f'Antal events i databasen: {len(events)}')
        
        # Vis eksempler på events
        print('\nEksempler på events:')
        for e in events[:5]:
            print(f'- {e.title_da} ({e.start_date} - {e.end_date})')
        
        # Tjek fremtidige events
        future_events = Event.query.filter(
            Event.end_date >= datetime.now()
        ).order_by(Event.start_date).all()
        
        print(f'\nAntal fremtidige events: {len(future_events)}')
        print('Eksempler på fremtidige events:')
        for e in future_events[:5]:
            print(f'- {e.title_da} ({e.start_date} - {e.end_date})')
        
        # Tjek events med billeder
        events_with_images = Event.query.filter(Event.image.isnot(None)).all()
        print(f'\nAntal events med billeder: {len(events_with_images)}')

if __name__ == '__main__':
    verify_events()
