import os
import pickle
import txtai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from .config import URL

CHROMA_PATH="src/rag_pdfs/chroma"
EMBEDDINGS_FILE = "src/rag_pdfs/embeddings.pkl"

def embedding_modele():
    embeddings = OllamaEmbeddings(model="nomic-embed", base_url=URL)
    #embeddings = txtai.Embeddings(path="neuml/pubmedbert-base-embeddings", content=True)#specifique au domaine medicale. Le modèle est basé sur BERT et a été spécifiquement pré-entraîné sur un corpus de données provenant de PubMed
    return embeddings

#extraire le texte du document passé en paramètre
def get_document_text(document):
    """Extrait le texte d'un objet Document."""
    if hasattr(document, 'page_content'):
        return document.page_content
    elif hasattr(document, 'content'):
        return document.content
    elif hasattr(document, 'text'):
        return document.text
    elif isinstance(document, dict) and 'text' in document:
        return document['text']
    elif isinstance(document, dict) and 'content' in document:
        return document['content']
    else:
        raise AttributeError("Impossible de trouver le contenu textuel du document")

#Calcule explicitement les embeddings pour les nouveaux chunks

def get_embedding(model, document):
    text = get_document_text(document)
    if hasattr(model, 'embed_query'):
        return model.embed_query(text)
    elif hasattr(model, 'embed_documents'):
        return model.embed_documents([text])[0]  # embed_documents attend une liste
    else:
        raise AttributeError("Le modèle d'embedding n'a pas de méthode 'embed_query' ou 'embed_documents'")


# fonction pour charger les embeddings existants 
def load_embeddings():
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# fonction pour sauvgarder les embeddings
def save_embeddings(new_embeddings):
     # Charger les embeddings existants
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "rb") as f:
            existing_embeddings = pickle.load(f)
    else:
        existing_embeddings = {}

    # Mettre à jour les embeddings existants avec les nouveaux
    existing_embeddings.update(new_embeddings)

    # Sauvegarder les embeddings mis à jour
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(existing_embeddings, f)


################# ids pour les chunks ############################################

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 1

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 1

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


############# faire l'embedding et sauvgarder dans une base de donnée #####################

def embedding(chunks, existing_embeddings):
    try:
        # Vérifier si le modèle d'embedding a déjà été chargé
        if not hasattr(embedding, 'embedding_model'):
            embedding.embedding_model = embedding_modele()  # Charger le modèle une seule fois
        
        # Charger la base existante
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding.embedding_model)

        # Calculer les IDs des chunks
        chunks_with_ids = calculate_chunk_ids(chunks)

        # Charger les documents existants dans la base de données
        existing_items = db.get(include=[]) #Récupère les IDs des documents déjà présents dans la base de données.
        existing_ids = set(existing_items["ids"]) #Convertit ces IDs en un ensemble pour une recherche plus rapide
        print(f"Nombre des documents existants dans DB: {len(existing_ids)}")

        # Filtrage des nouveaux documents à ajouter 
        #  filtre les chunks pour ne garder que ceux qui ne sont pas déjà présents dans la base de données
        new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

        # si pas de nouveaux 
        if not new_chunks:
            print("-> pas d'ajout de nouveaux documents")
            return db, existing_embeddings  # Retourner immédiatement si aucun nouveau chunk

        new_embeddings = {}
        for chunk in new_chunks:
            chunk_id = chunk.metadata["id"]
            if chunk_id not in existing_embeddings: #Pour chaque nouveau chunk, vérifie si son embedding existe déjà.
                new_embeddings[chunk_id] = get_embedding(embedding.embedding_model, chunk) # on fait l'embedding des nouveaux

        # Ajouter les nouveaux documents à la base de données
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids, embeddings=[new_embeddings[chunk_id] for chunk_id in new_chunk_ids])

        print(f"Embedded {len(new_chunks)} nouveaux chunks et sauvgarder dans chroma")
        return db, new_embeddings # retourne les nouveaux pour les sauvgarder apres 

    except Exception as e:
        print(f"une error : {str(e)}")
        return None, existing_embeddings


