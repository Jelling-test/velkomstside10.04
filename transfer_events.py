import os
import sys
import sqlite3
from datetime import datetime
import json

# Sti til den gamle database
OLD_DB_PATH = r'C:\Users\peter\Desktop\velkomstside\instance\jelling_camping.db'
NEW_DB_PATH = r'C:\Users\peter\CascadeProjects\JellingCampingVelkomst\instance\app.db'

def get_table_info(db_path):
    """Henter information om tabeller i databasen"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    table_info = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        table_info[table] = columns
    
    conn.close()
    return table_info

def get_events_from_old_db():
    """Henter events fra den gamle database"""
    conn = sqlite3.connect(OLD_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Find events-tabellen
    table_info = get_table_info(OLD_DB_PATH)
    event_table = None
    
    for table, columns in table_info.items():
        if 'title' in columns and 'start_date' in columns and 'end_date' in columns:
            event_table = table
            break
    
    if not event_table:
        print("Kunne ikke finde events-tabellen i den gamle database")
        return []
    
    print(f"Fandt events-tabellen: {event_table}")
    
    # Hent alle events fra den gamle database
    cursor.execute(f'SELECT * FROM {event_table}')
    events = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return events

def insert_events_to_new_db(events):
    """Indsætter events i den nye database"""
    conn = sqlite3.connect(NEW_DB_PATH)
    cursor = conn.cursor()
    
    # Find events-tabellen i den nye database
    table_info = get_table_info(NEW_DB_PATH)
    event_table = None
    
    for table, columns in table_info.items():
        if 'title_da' in columns and 'start_date' in columns and 'end_date' in columns:
            event_table = table
            break
    
    if not event_table:
        print("Kunne ikke finde events-tabellen i den nye database")
        return
    
    print(f"Fandt events-tabellen i den nye database: {event_table}")
    
    # Få kolonnenavnene for den nye events-tabel
    cursor.execute(f"PRAGMA table_info({event_table})")
    new_columns = [row[1] for row in cursor.fetchall()]
    
    # Indsæt hver event i den nye database
    for event in events:
        # Tjek om eventet allerede findes
        cursor.execute(f"SELECT id FROM {event_table} WHERE title_da = ? AND start_date = ?", 
                      (event.get('title', ''), event.get('start_date', '')))
        existing = cursor.fetchone()
        
        if existing:
            print(f"Event '{event.get('title', '')}' findes allerede i den nye database")
            continue
        
        # Opret et dictionary med de korrekte kolonnenavne for den nye database
        new_event = {}
        
        # Mapping mellem gamle og nye kolonnenavne
        mapping = {
            'title': 'title_da',
            'title_en': 'title_en',
            'title_de': 'title_de',
            'title_nl': 'title_nl',
            'description': 'description_da',
            'description_en': 'description_en',
            'description_de': 'description_de',
            'description_nl': 'description_nl',
            'start_date': 'start_date',
            'end_date': 'end_date',
            'image_path': 'image'
        }
        
        for old_col, new_col in mapping.items():
            if old_col in event and new_col in new_columns:
                value = event[old_col]
                
                # Håndter billedsti
                if old_col == 'image_path' and value:
                    # Udtræk kun filnavnet fra stien
                    value = value.split('/')[-1] if '/' in value else value
                
                new_event[new_col] = value
        
        # Tilføj is_active = True
        if 'is_active' in new_columns:
            new_event['is_active'] = 1
        
        # Opret SQL til indsætning
        columns = ', '.join(new_event.keys())
        placeholders = ', '.join(['?' for _ in new_event])
        values = list(new_event.values())
        
        sql = f"INSERT INTO {event_table} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor.execute(sql, values)
            print(f"Tilføjet event: {event.get('title', '')}")
        except Exception as e:
            print(f"Fejl ved indsætning af event '{event.get('title', '')}': {e}")
    
    # Gem ændringerne
    conn.commit()
    conn.close()
    print("Alle events er blevet overført")

def main():
    print("Starter overførsel af events fra den gamle til den nye database...")
    
    # Tjek om databaserne eksisterer
    if not os.path.exists(OLD_DB_PATH):
        print(f"Fejl: Den gamle database findes ikke på stien: {OLD_DB_PATH}")
        return
    
    if not os.path.exists(NEW_DB_PATH):
        print(f"Fejl: Den nye database findes ikke på stien: {NEW_DB_PATH}")
        return
    
    # Hent events fra den gamle database
    events = get_events_from_old_db()
    print(f"Fandt {len(events)} events i den gamle database")
    
    # Indsæt events i den nye database
    insert_events_to_new_db(events)

if __name__ == '__main__':
    main()
