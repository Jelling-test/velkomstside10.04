FROM python:3.11-slim

# Installer nødvendige systemafhængigheder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Opret arbejdsmappe
WORKDIR /app

# Kopier requirements først (for bedre cache-udnyttelse)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopier resten af applikationen
COPY . .

# Opret mapper til uploads og database hvis de ikke findes
RUN mkdir -p app/static/uploads/menu \
    && mkdir -p app/static/uploads/bakery \
    && mkdir -p app/static/uploads/events \
    && mkdir -p app/static/uploads/posters \
    && mkdir -p instance

# Sæt rettigheder på mapper
RUN chmod 777 app/static/uploads/menu \
    && chmod 777 app/static/uploads/bakery \
    && chmod 777 app/static/uploads/events \
    && chmod 777 app/static/uploads/posters \
    && chmod 777 instance

# Eksponér port
EXPOSE 5000

# Kør Gunicorn som produktions-webserver
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
