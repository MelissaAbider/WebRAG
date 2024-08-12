import os
import hashlib
import pickle
import shutil  # Pour copier des fichiers
from rag_pdfs.documents_load import load_pdfs
from rag_pdfs.chunking import split_text


# Fichier pour suivre les fichiers traités
STATE_FILE = "src/rag_pdfs/processed_files.txt"
# Fichier pour stocker les chunks
CHUNKS_FILE = "src/rag_pdfs/chunks.pkl"

#retourne un hash du contenu du fichier pour détecter les modifications.
def get_file_hash(file_path):
    
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# charge les fichiers déjà traités depuis le fichier d'état
def load_processed_files():
   
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return {line.strip(): get_file_hash(line.strip()) for line in f}
    return {}

#Ajoute le fichier traité au fichier d'état
def save_processed_file(file_path):
    
    with open(STATE_FILE, "a") as f:
        f.write(file_path + "\n")

#Charge les chunks depuis le fichier
def load_chunks():
    
    if os.path.exists(CHUNKS_FILE):
        with open(CHUNKS_FILE, "rb") as f:
            return pickle.load(f)
    return []

#Sauvegarde les nouveaux chunks dans un fichier
def save_chunks(chunks):
    
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

#Charge tous les nouveaux documents dans le répertoire (pour pouvoir utiliser la fonction load_pdfs qui prend le nom d'un repertoire contenant des pdf ) et retourne les chunks
def process_documents_in_directory(directory):
    
    processed_docs = load_pdfs(directory)  
    return split_text(processed_docs)
