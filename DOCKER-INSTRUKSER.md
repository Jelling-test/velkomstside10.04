# Docker-instruktioner til Jelling Camping Velkomstside

Denne vejledning beskriver, hvordan du kan deploye Jelling Camping Velkomstsiden på en NAS ved hjælp af Docker.

## Forudsætninger

- En NAS med Docker-support (f.eks. Synology, QNAP)
- Adgang til NAS via SSH eller filoverførsel
- Grundlæggende kendskab til kommandolinjen

## Trin for deployment

### 1. Overfør filer til NAS

Overfør hele projektmappen til din NAS. Du kan bruge SCP, SFTP eller din NAS's filhåndteringsværktøj.

```bash
# Eksempel på overførsel med SCP (fra en Linux/Mac terminal)
scp -r /sti/til/JellingCampingVelkomst bruger@nas-ip:/destination/sti
```

### 2. Opret .env fil

Opret en `.env` fil i projektmappen med følgende miljøvariabler:

```
# Flask konfiguration
SECRET_KEY=din_hemmelige_nøgle_her
FLASK_APP=app.py
FLASK_ENV=production

# Database konfiguration
DB_HOST=192.168.1.254
DB_USER=windsurf
DB_PASSWORD=7300Jelling!
DB_NAME=camping_aktiv

# Email konfiguration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=peter@jellingcamping.dk
SMTP_PASSWORD=etde mpln hwia doxh
EMAIL_FROM=info@jellingcamping.dk

# Admin legitimationsoplysninger
ADMIN_USERNAME=admin
ADMIN_PASSWORD=JellingCamping2023!

# Bager bestillingstider
BAKERY_ORDER_START_TIME=10
BAKERY_ORDER_END_TIME=5
```

### 3. Byg og start Docker-containeren

Log ind på din NAS via SSH og naviger til projektmappen:

```bash
cd /sti/til/JellingCampingVelkomst
```

Start containeren med docker-compose:

```bash
docker-compose up -d
```

Dette vil bygge Docker-imaget og starte containeren i baggrunden.

### 4. Initialiser databasen

Når containeren kører, skal du initialisere databasen:

```bash
docker exec -it jelling_camping_velkomst flask db init
docker exec -it jelling_camping_velkomst flask db migrate -m "Initial migration"
docker exec -it jelling_camping_velkomst flask db upgrade
```

### 5. Opret admin-bruger

Opret en admin-bruger til systemet:

```bash
docker exec -it jelling_camping_velkomst flask create-admin
```

## Specifikt for Synology NAS

### Installation via Docker GUI

1. Åbn Docker-pakken på din Synology NAS
2. Gå til "Registrering" > "Lokalt"
3. Klik på "Byg" og vælg mappen med projektet
4. Følg vejledningen på skærmen for at bygge imaget
5. Gå til "Container" > "Opret"
6. Vælg det byggede image og konfigurer containeren:
   - Tilføj miljøvariabler fra .env filen
   - Konfigurer port-mapping (5000:5000)
   - Konfigurer volume-mapping for /app/instance og /app/app/static/uploads

## Vedligeholdelse

### Genstart containeren

```bash
docker-compose restart
```

### Se logs

```bash
docker-compose logs -f
```

### Opdatering

Når du har ændringer i koden:

1. Overfør de nye filer til NAS'en
2. Genbyg og genstart containeren:

```bash
docker-compose down
docker-compose up -d --build
```

## Fejlfinding

### Container starter ikke

Tjek logs for fejl:

```bash
docker-compose logs
```

### Database-problemer

Hvis der er problemer med databasen, kan du prøve at køre migrationer igen:

```bash
docker exec -it jelling_camping_velkomst flask db upgrade
```

### Tilladelser

Hvis der er problemer med filrettigheder:

```bash
docker exec -it jelling_camping_velkomst chmod -R 777 /app/instance
docker exec -it jelling_camping_velkomst chmod -R 777 /app/app/static/uploads
```

## Sikkerhedsovervejelser

- Ændr standardadgangskoden for admin-brugeren
- Brug en stærk SECRET_KEY
- Overvej at bruge HTTPS med en reverse proxy foran applikationen
- Begræns adgang til Docker-containeren fra netværket
