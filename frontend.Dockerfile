FROM nginx:latest

ARG ENV

WORKDIR /usr/share/nginx/html
# Copie les fichiers front-end dans le répertoire de Nginx
COPY src/front .

# If the environment is production, modify the script.js file
RUN if [ "$ENV" = "production" ]; then \
    sed -i 's|http://localhost:8000|https://api.llm-rag.aidd4h.checksem.fr|g' ./script.js; \
    fi

# Copie le fichier de configuration Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Expose le port de Nginx, le conteneur écoutera sur le port 80
EXPOSE 80
