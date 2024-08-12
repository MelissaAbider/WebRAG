#pip install sqlalchemy

from sqlalchemy.orm import Session
from .models import Prompt
#from models import Prompt
from .schemas import PromptCreate
from api_bd import models
#from schemas import PromptCreate
#Définir les opérations CRUD (Create, Read, Update, Delete) les données dans la base de données

'''Cette fonction prend un objet `PromptCreate` contenant les détails du prompt et l'ajoute à la base de données'''
def create_prompt(db: Session, prompt: PromptCreate):
    db_prompt = Prompt(
        question=prompt.question, 
        answer=prompt.answer,
        context=prompt.context,
        source=prompt.source,
        comment=prompt.comment,
        rating=prompt.rating
        
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

'''Cette fonction interroge la base de données pour trouver un prompt correspondant à l'id'''
def get_prompt(db: Session, prompt_id: int):
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()
