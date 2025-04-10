import sqlite3
import os

# Forbind til databasen
conn = sqlite3.connect('instance/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Hent events med billeder
cursor.execute('SELECT id, title_da, image FROM event WHERE image IS NOT NULL LIMIT 10')
events = cursor.fetchall()

print("Sammenligner filnavne i databasen med faktiske filer:")
print("-" * 50)

# Få liste over filer i uploads/events mappen
event_files = os.listdir(os.path.join('app', 'static', 'uploads', 'events'))
print(f"Filer i uploads/events mappen: {len(event_files)}")
for i, filename in enumerate(event_files[:5]):
    print(f"{i+1}. {filename}")
print("...")

print("\nEvents i databasen:")
for event in events:
    event_id = event['id']
    title = event['title_da']
    image = event['image']
    
    # Tjek om billedet findes i mappen
    file_exists = image in event_files
    
    print(f"ID: {event_id}, Titel: {title[:20]}..., Billede: {image}, Findes: {file_exists}")

conn.close()
