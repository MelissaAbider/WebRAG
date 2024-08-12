from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# Définition de l'URL de la base de données
#DATABASE_URL = "sqlite:///sql_app.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/src/api_bd/sql_app.db")# Récupérer l'URL de la base de données depuis les variables d'environnement
# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Création de la classe SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base pour les modèles
Base = declarative_base()

#fonction qui réinitialiser la base de données
'''def reset():

    from models import Prompt  # Importer ici pour éviter les imports circulaires
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("La base de données a été réinitialisée avec succès.")'''

