import random
import csv
import io
from http.client import HTTPException

from fastapi import FastAPI, Depends #Le framework pour construire l'API,depends :Pour gérer les dépendances, comme la session de base de données.
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session #Pour interagir avec la base de données via SQLAlchemy
from sqlalchemy import select

#from . import models, schemas, crud # Modules personnalisés pour les modèles de données, les schémas de validation, et les opérations CRUD
from .database import engine, SessionLocal #Pour la configuration de la base de données
from api_bd import models
from api_bd import schemas
from api_bd import crud
from rag_pdfs.main import main 
from rag_pdfs.without_rag import query_without_rag
from .models import Base  # Assurez-vous d'importer vos modèles


# Créer les tables dans la base de données définies dans les modèles
def init_db():
    #Base.metadata.drop_all(bind=engine)  # Supprime toutes les tables existantes si besoin 
    Base.metadata.create_all(bind=engine)  # Crée toutes les tables

# Appelez cette fonction au démarrage 
init_db()

#Initialise l'application FastAPI.
app = FastAPI()

# fournit une session de base de données.
def get_db():
    db = SessionLocal() #Crée une instance de la session de base de données locale
    try:
        yield db #Fournit la session de base de données à la route qui en a besoin
    #return db #Fournit la session de base de données à la route qui en a besoin
    finally:
         db.close() #Ferme la session de base de données une fois que la route a terminé.

@app.get("/api/")
async def read_api():
    return {"message": "API is working!"}

# le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par les origines autorisées si nécessaire
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes, y compris OPTIONS
    allow_headers=["*"],  # Autorise tous les en-têtes
)

'''Cette fonction est appelée lorsque l'utilisateur envoie une question via l'API.
Elle crée un nouvel objet Prompt dans la base de données '''

@app.post("/api/ask/", response_model=schemas.Prompt)
def ask_question(question: schemas.Question, db: Session = Depends(get_db)):

    # Créer un nouvel objet PromptCreate avec les données de la question
    prompt_create = schemas.PromptCreate(
        question=question.question,  # Utiliser le champ question
        answer="",  # Laisser vide pour l'instant
        context="",  # Contexte (à modifier après)
        source="" ,  # Laisser vide pour l'instant
        comment="", #commentaire vide au debut 
        rating=0 #notation vide au debut 
    )
    
    # Créer le prompt dans la base de données
    stored_prompt = crud.create_prompt(db=db, prompt=prompt_create)

    # Déterminer si on utilise RAG ou LLM
    if random.random() < 0.67:  # 2/3 des cas pour RAG
        answer, sources = main(question.question)  # Utiliser RAG
        stored_prompt.context = "LLM+RAG"

    else:  # 1/3 des cas pour LLM
        answer = query_without_rag(question.question)  # Utiliser LLM
        stored_prompt.context = "LLM seul"
        sources = []  # Pas de sources quand cest le LLM seul qui repond

    # Mettre à jour le prompt avec la réponse générée
    stored_prompt.answer = answer
    stored_prompt.source = ", ".join(sources)  # Joindre les sources en une seule chaîne

    # Sauvegarder les modifications dans la base de données
    db.commit()  
    db.refresh(stored_prompt)  # Rafraîchir l'instance pour obtenir les données mises à jour

    return stored_prompt  # Retourner l'objet Prompt mis à jour


'''Cette fonction est appelée lorsque l'utilisateur soumet un feedback (commentaire + rating) pour un
prompt spécifique via l'API. Elle met à jour le prompt correspondant (grace à son id) dans la base de données '''

# on utilise l'id du prompte precendant pour recuperer son feedback
@app.post("/api/feedback/{prompt_id}", response_model=schemas.Prompt)
def add_feedback(prompt_id: int, feedback: schemas.FeedbackUpdate, db: Session = Depends(get_db)):
    stored_prompt = crud.get_prompt(db, prompt_id) #Tente de récupérer le prompt avec l'ID fourni
    if not stored_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    #Met à jour les champs commentaire et rating du prompt stocké avec les nouvelles valeurs
    stored_prompt.comment = feedback.comment # mettre à jour le prompte avec le commentaire 
    stored_prompt.rating = feedback.rating  # mettre à jour le prompte avec la notation

    db.commit()
    db.refresh(stored_prompt) # Rafraîchir l'instance pour obtenir les données mises à jour

    return stored_prompt # Retourner l'objet Prompt mis à jour

@app.get("/api/export_csv")
def export_data_to_csv(db: Session = Depends(get_db)):
    prompts = db.execute(select(models.Prompt)).scalars().all()

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    # Write header
    writer.writerow(['id', 'question', 'answer', 'context', 'source', 'comment', 'rating'])
    # Write data
    for prompt in prompts:
        writer.writerow([prompt.id, prompt.question, prompt.answer, prompt.context, prompt.source, prompt.comment, prompt.rating])

    output.seek(0)  # Reset the pointer to the start of the stream
    return StreamingResponse(output, media_type='text/csv', headers={"Content-Disposition": "attachment; filename=prompts.csv"})
