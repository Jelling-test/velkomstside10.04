import sqlite3

# Sti til den gamle database
OLD_DB_PATH = r'C:\Users\peter\Desktop\velkomstside\instance\jelling_camping.db'

def check_tables():
    """Undersøger tabeller i databasen"""
    conn = sqlite3.connect(OLD_DB_PATH)
    cursor = conn.cursor()
    
    # Hent alle tabeller
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    table_names = [table[0] for table in tables]
    print(f"Tabeller i databasen ({len(table_names)}):")
    for table_name in table_names:
        print(f"- {table_name}")
    
    # Søg efter calendar eller event tabeller
    calendar_tables = [t for t in table_names if 'calendar' in t.lower() or 'event' in t.lower()]
    if calendar_tables:
        print("\nFandt følgende kalender/event tabeller:")
        for table_name in calendar_tables:
            print(f"- {table_name}")
            
            # Hent kolonner for denne tabel
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"  Kolonner: {[col[1] for col in columns]}")
            
            # Hent antal rækker
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Antal rækker: {count}")
            
            # Hvis tabellen har rækker, vis et eksempel
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                row = cursor.fetchone()
                example = {}
                for i, col in enumerate(columns):
                    if i < len(row):
                        example[col[1]] = row[i]
                print(f"  Eksempel på række: {example}")
    else:
        print("\nIngen kalender/event tabeller fundet.")
    
    conn.close()

if __name__ == '__main__':
    check_tables()
