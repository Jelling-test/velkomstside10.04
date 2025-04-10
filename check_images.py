import sqlite3

# Forbind til databasen
conn = sqlite3.connect('instance/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Hent events med billeder
cursor.execute('SELECT id, title_da, image FROM event')
events = cursor.fetchall()

# Skriv resultatet til en fil
with open('event_images.txt', 'w') as f:
    f.write('Alle events:\n')
    for event in events:
        f.write(f'ID: {event["id"]}, Titel: {event["title_da"]}, Billede: {event["image"]}\n')

print(f"Informationer om {len(events)} events er gemt i filen 'event_images.txt'")

conn.close()
