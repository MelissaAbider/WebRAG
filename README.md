# RAGWeb

RAGWeb est une application web qui utilise la génération augmentée par récupération (RAG) pour répondre aux questions des utilisateurs. L'application permet aux utilisateurs de poser des questions via une interface web, de recevoir des réponses générées par le système RAG, et de fournir des retours sur les réponses. Toutes les interactions, y compris les questions, les réponses et les retours, sont stockées dans une base de données SQLite.

## Fonctionnalités

### Interface Web
Permet aux utilisateurs de poser des questions et de recevoir des réponses.

### Génération Augmentée par Récupération (RAG)
Utilise des techniques avancées pour fournir des réponses précises et informées.

### Feedback Utilisateur
Les utilisateurs peuvent donner leur avis sur les réponses fournies (un commentaire + note de 1 à 5).

### Stockage des Interactions
Les questions, réponses et feedbacks sont stockés dans une base de données SQLite pour analyse ultérieure.

## Technologies Utilisées

- **FastAPI** : Framework web rapide et moderne pour construire l'API backend.
- **SQLite** : Base de données légère pour stocker les interactions utilisateur.
- **HTML/CSS/JavaScript** : Pour l'interface utilisateur front-end.
- **Ollama et Mistral** : Ollama est utilisé pour déployer localement le modèle Mistral 7B, un grand modèle de langage compact et performant.
- **Chroma** : Base de données vectorielle pour stocker et récupérer les embeddings (les représentations vectorielles des documents utilisés pour le RAG).
- **Docker & Docker Compose** : Pour conteneuriser l'application et gérer les services.

## Lancement

### Lancer l'application avec Docker Compose

Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine. Lancez cette commande :

```bash
docker-compose up --build
