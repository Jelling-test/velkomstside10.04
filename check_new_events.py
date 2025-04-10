import sqlite3
from datetime import datetime

# Sti til den nye database
DB_PATH = r'C:\Users\peter\CascadeProjects\JellingCampingVelkomst\instance\app.db'

def check_events():
    """Undersøger events i den nye database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Hent antal events
    cursor.execute("SELECT COUNT(*) FROM event")
    count = cursor.fetchone()[0]
    print(f"Antal events i databasen: {count}")
    
    # Vis eksempler på events
    cursor.execute("SELECT id, title_da, title_en, start_date, end_date, image FROM event LIMIT 5")
    events = cursor.fetchall()
    
    print("\nEksempler på events:")
    for event in events:
        print(f"- {event['title_da']} ({event['start_date']} - {event['end_date']})")
        print(f"  Engelsk titel: {event['title_en']}")
        print(f"  Billede: {event['image']}")
    
    # Tjek fremtidige events
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"SELECT COUNT(*) FROM event WHERE end_date >= '{now}'")
    future_count = cursor.fetchone()[0]
    print(f"\nAntal fremtidige events: {future_count}")
    
    # Tjek events med billeder
    cursor.execute("SELECT COUNT(*) FROM event WHERE image IS NOT NULL AND image != ''")
    with_image_count = cursor.fetchone()[0]
    print(f"Antal events med billeder: {with_image_count}")
    
    conn.close()

if __name__ == '__main__':
    check_events()
