# Jelling Camping Velkomstside

Dette er en Flask-applikation, der fungerer som velkomstside for Jelling Camping. Applikationen er designet til at være mobiloptimeret og giver gæsterne mulighed for at se information om campingpladsen, bestille rundstykker, se menukort og tilmelde sig arrangementer.

## Funktioner

### Offentlig del
- Forside med velkomstbesked og campingpladsinfo
- Sprogvælger (dansk, engelsk, tysk, hollandsk, finsk, norsk, svensk)
- Café-sektion med menukort, åbningstider og specialtilbud
- Aktiviteter og events kalender

### Brugerområde (kræver login)
- Login-system baseret på booking-nummer og efternavn
- Bestilling af rundstykker og specialtilbud
- Tilmelding til arrangementer

### Admin-område
- Dashboard med oversigt
- Administration af café-menu, bager, kalender og kampagner

## Installation

1. Klon dette repository
2. Opret et virtuelt miljø: `python -m venv venv`
3. Aktiver det virtuelle miljø:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Installer afhængigheder: `pip install -r requirements.txt`
5. Opret en `.env`-fil med de nødvendige miljøvariabler (se eksempel i `.env.example`)
6. Initialiser databasen: `flask db init`, `flask db migrate`, `flask db upgrade`
7. Start applikationen: `flask run`

## Miljøvariabler

Applikationen kræver følgende miljøvariabler, som kan defineres i en `.env`-fil:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=en_sikker_noegle

# Database konfiguration
DB_HOST=localhost
DB_USER=bruger
DB_PASSWORD=adgangskode
DB_NAME=database_navn

# Booking database konfiguration
BOOKING_DB_HOST=localhost
BOOKING_DB_USER=bruger
BOOKING_DB_PASSWORD=adgangskode
BOOKING_DB_NAME=booking_database

# Email konfiguration
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=bruger@example.com
SMTP_PASSWORD=adgangskode
EMAIL_FROM=info@example.com

# Admin bruger
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sikker_adgangskode

# Bestillingstider for rundstykker
BAKERY_ORDER_START_TIME=10
BAKERY_ORDER_END_TIME=5
```

## Projektstruktur

```
JellingCampingVelkomst/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── templates/
│       ├── admin/
│       ├── auth/
│       └── main/
├── migrations/
├── .env
├── .gitignore
├── app.py
├── config.py
└── requirements.txt
```

## Udvikling

For at starte applikationen i udviklingstilstand:

```
flask run
```

For at oprette en ny database-migration efter ændringer i modeller:

```
flask db migrate -m "Beskrivelse af ændringer"
flask db upgrade
```
