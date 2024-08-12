

from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Définit les modèles de données pour les prompts
#Les modèles utilisent SQLAlchemy pour définir les tables et les relations entre elles

#Cette base sera utilisée pour définir les modèles de données
Base = declarative_base()

'''Cette classe définit la structure de la table 'prompts' dans la base de données'''
class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)
    question = Column(Text) #la questioon de l'utilisateur
    answer = Column(Text) # la reponse généré par le LLM ou RAG+LLM
    context = Column(Text) # llm ou llm+rag
    source = Column(String)  # les chunks utiliser si cest le rag+llm
    comment = Column(Text,default="")    # Commentaire de feedback 
    rating = Column(Integer,default=0) # la notation (les etoiles ) 

