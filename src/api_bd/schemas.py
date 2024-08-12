
from typing import Optional
from pydantic import BaseModel #bibliothèque Python qui fournit un ensemble de outils pour valider et parser des données
from datetime import datetime #bibliothèque Python qui fournit des outils pour travailler avec des dates et des heures


#les schémas sont utilisés pour valider les données d'entrée et de sortie des API

#créer un nouveau prompt dans la base de données
class PromptCreate(BaseModel):
    question: str
    answer: str = ""
    context: str 
    source: str = ""
    comment: str = ""
    rating: int = 0

#utilisé pour retourner un prompt complet, y compris les champs de feedback
class Prompt(BaseModel):
    id: int
    question: str
    answer: str
    context: str 
    source: str
    comment: str=""
    rating: int =0
    class Config:
        orm_mode = True

#utilisé lorsque l'utilisateur envoie une question à l'API
class Question(BaseModel):
    question: str

#utilisé lorsque l'utilisateur envoie un feedback après avoir reçu une réponse
class FeedbackUpdate(BaseModel):
    comment: str = None
    rating: int = None
