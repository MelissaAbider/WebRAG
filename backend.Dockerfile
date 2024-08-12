FROM python:3.9

#Définit le répertoire de travail à /app dans le conteneur. Toutes les commandes suivantes s'exécuteront dans ce répertoire
WORKDIR /app

#Copie le fichier requirements.txt du répertoire local vers le répertoire de travail du conteneur
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#Copie tout le contenu du répertoire src du projet local vers le répertoire /app/src du conteneur
COPY src /app/src

ENV PYTHONPATH=/app/src

#Indique que le conteneur écoutera sur le port 8000.
EXPOSE 8000

CMD ["uvicorn", "src.api_bd.main:app", "--host", "0.0.0.0", "--port", "8000"]
