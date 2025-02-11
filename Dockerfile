FROM ubuntu:latest

# Mettre à jour le système et installer Python et venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY secure_notes.py ./
COPY key.txt ./

# Créer un environnement virtuel et installer les dépendances
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir cryptography

# Créer le répertoire de stockage des notes chiffrées
RUN mkdir -p /data/secure_files

# Définir la commande par défaut pour exécuter le script
ENTRYPOINT ["/app/venv/bin/python", "secure_notes.py"]
