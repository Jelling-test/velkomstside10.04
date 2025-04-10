import sqlite3
import os

# Forbind til databasen
conn = sqlite3.connect('instance/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Hent events med billeder
cursor.execute('SELECT id, title_da, image FROM event WHERE image IS NOT NULL')
events = cursor.fetchall()

print(f"Opdaterer billedstier for {len(events)} events...")
for event in events:
    event_id = event['id']
    title = event['title_da']
    image_path = event['image']
    
    # Få filnavnet uden sti
    filename = os.path.basename(image_path) if '/' in image_path else image_path
    
    # Opdater billedstien i databasen
    cursor.execute('UPDATE event SET image = ? WHERE id = ?', (filename, event_id))
    print(f"ID: {event_id}, Titel: {title}, Opdateret billede: {filename}")

# Gem ændringerne
conn.commit()
conn.close()

print("Alle billedstier er blevet opdateret til kun at indeholde filnavnet.")
