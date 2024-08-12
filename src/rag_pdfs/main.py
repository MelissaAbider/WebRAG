

from rag_pdfs.embedding import embedding
from rag_pdfs.query import query_rag
import os
import sys
import shutil  # Pour copier des fichiers
from rag_pdfs.utils import load_processed_files, save_processed_file, load_chunks, save_chunks,process_documents_in_directory,get_file_hash
import requests
from  rag_pdfs.embedding import save_embeddings,load_embeddings, embedding_modele
from langchain_community.vectorstores import Chroma
from .config import URL

CHROMA_PATH="src/rag_pdfs/chroma"
DATA_PATH = "src/rag_pdfs/documents_complets"# Chemin vers le répertoire des documents
TEMP_DIR = "src/rag_pdfs/temp_documents"# Répertoire temporaire pour le traitement


def main(prompt) -> str:
    # Charger l'état des fichiers traités
    processed_files = load_processed_files()
    new_files = []

    # parcourt le répertoire et détecte les fichiers nouveaux ou modifiés en comparant leurs hashes avec ceux des fichiers traités
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path) # calcule le hash MD5 du contenu d'un fichier pour détecter les changements

            # Si le fichier est nouveau, l'ajouter à la liste
            if file_path not in processed_files or processed_files[file_path] != file_hash:
                new_files.append(file_path)

    # Charger les chunks existants (pas vraiment besoin pour la nouvelle version)
    #existing_chunks = load_chunks()

    # dans le cas ou on a des nouveaux fichiers #######################################

    if new_files:
        print("Nouveaux fichiers détectés, traitement en cours...")

        # Charger les embeddings existants
        existing_embeddings = load_embeddings()

        # Créer un répertoire temporaire
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        # Copier les nouveaux fichiers dans le répertoire temporaire
        for file in new_files:
            shutil.copy(file, TEMP_DIR)

        # Traiter les documents dans le répertoire temporaire
        new_chunks = process_documents_in_directory(TEMP_DIR)

        # Sauvegarder les nouveaux chunks
        save_chunks(new_chunks)

        # Embedding des nouveaux chunks
        vectorstore, new_embeddings = embedding(new_chunks, existing_embeddings)

        # Enregistrer les nouveaux embeddings
        save_embeddings(new_embeddings)

        # Enregistrer tous les fichiers traités
        for file in new_files:
            save_processed_file(file)

        # Supprimer le répertoire temporaire après traitement
        shutil.rmtree(TEMP_DIR)

    # dans le cas ou on a pas des nouveaux fichiers #######################################

    # on a pas besoin de faire l'embedding car cest déja present dans chroma
    else:
        print("Aucun nouveau document détecté, utilisation des chunks existants.")

        #vectorstore, _ = embedding(existing_chunks, existing_embeddings)
        # juste verifier le nombres d'elemnts dans chroma 
        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_modele())
        existing_items = vectorstore.get(include=[])
        document_count = len(existing_items["ids"])
        print(f"Nombre de documents dans la base de données : {document_count}")


    # Utiliser RAG pour interroger la base de données 
    print("\n########\n with RAG\n")
    result_with_rag,sources = query_rag(prompt)# renvoie le resultat et les sources separés
    #print(result_with_rag)
    return result_with_rag,sources

################# initialisation de mitral et nomic ##########################"

def init_mistral():
    print('Initializing ollama model')

    # read modelfile as str
    with open("src/rag_pdfs/Modelfile", "r") as f:
        model = f.read()

        prompt_data = {
            "name": "mistral-ollama",
            "modelfile": model
        }

        response = requests.post(URL+"/api/create", json=prompt_data)
        print(response.text)

    print('Done initializing ollama model')

def init_nomic():
    print('Initializing nomic model')

    # read modelfile as str
    with open("src/rag_pdfs/Modelfile.embeddings", "r") as f:
        model = f.read()

        prompt_data = {
            "name": "nomic-embed",
            "modelfile": model
        }

        response = requests.post(URL+"/api/create", json=prompt_data)
        print(response.text)

    print('Done initializing nomic model')




if __name__ == "__main__":
    if sys.argv[1]=="init":
        init_nomic()
        init_mistral()
   

    #prompt = sys.argv[1]
    #main(prompt)

#docker ps -a : lister tous les conteneurs (y compris ceux arrêtés)
 # acceder au front http://localhost
