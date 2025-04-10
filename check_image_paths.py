import sqlite3
import os

# Forbind til databasen
conn = sqlite3.connect('instance/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Hent events med billeder
cursor.execute('SELECT id, title_da, image FROM event')
events = cursor.fetchall()

# Tjek om billederne findes i den nye mappe
print(f"Tjekker {len(events)} events for billeder...")
for event in events:
    event_id = event['id']
    title = event['title_da']
    image_path = event['image']
    
    if image_path:
        # Tjek om billedet findes i uploads/events mappen
        base_filename = os.path.basename(image_path) if '/' in image_path else image_path
        full_path = os.path.join('app', 'static', 'uploads', 'events', base_filename)
        
        if os.path.exists(full_path):
            print(f"ID: {event_id}, Titel: {title}, Billede findes: {base_filename}")
        else:
            print(f"ID: {event_id}, Titel: {title}, Billede mangler: {base_filename}")
    else:
        print(f"ID: {event_id}, Titel: {title}, Intet billede angivet")

conn.close()
