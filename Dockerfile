# Base image Python
FROM python:3.11-slim

# Installer Python et pip
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer les dépendances Python
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier le script et les données
COPY script/ ./script/
COPY data/ ./data/

# Copier le fichier .env
COPY .env .env

# Définir le port MongoDB exposé
EXPOSE 27017

# Exécuter un script shell pour lancer les étapes de migration séquentiellement
CMD ["bash", "-c", "python3 ./script/data_cleaning.py && python3 ./script/migration.py && python3 ./script/test_post_migration.py"]

