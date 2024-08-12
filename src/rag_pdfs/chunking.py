from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document 
import re
from langchain_community.vectorstores import Chroma
from .config import URL

############# deviser en chunks #######################################

def split_text(documents: list[tuple[str, str, int]]):# prend en parametre une liste de tubles qui contiennent : le texte(du document pdf) , la source(le chemin vers ce fichier), et le numéro de page( de la page du document)
    print("chunking avec SemanticChunker")
    # on utilise le chunking semantic 
    text_splitter = SemanticChunker(OllamaEmbeddings(model="nomic-embed", base_url=URL), breakpoint_threshold_type="interquartile") #le découpage du texte doit se baser sur des statistiques interquartiles
    
    '''text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4",
        chunk_size=1500,
        chunk_overlap=10,
    )'''
    document_objects = [
        Document(page_content=text, metadata={"source": source, "page": page})
        for text, source, page in documents
    ] 
    chunks = text_splitter.split_documents(document_objects)
   
    print(f"deviser {len(documents)} documents en {len(chunks)} chunks.")
    '''try:
        i = 5
        if i < len(chunks):
            document = chunks[i]
            print(f"Contenu de la page : {document.page_content}")
        else:
            print(f"L'index {i} est en dehors de la plage valide pour le tableau")
    except IndexError:
        print(f"Erreur : L'index {i} est en dehors de la plage valide pour le tableau")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")'''

    return chunks


#methode 2 en ce basant sur les titres non complete 
'''
################### extraire les chunks en se basant sur les titres ##########################

def extract_sections(text, title_dict):
    # Créer un pattern regex pour capturer tous les titres
    all_titles = [title for variants in title_dict.values() for title in variants]
    pattern = '|'.join([re.escape(title) for title in all_titles])
    
    # Ajouter des parenthèses pour capturer les titres dans le texte
    pattern = f'({pattern})'
    
    # Utiliser re.split pour diviser le texte en sections
    parts = re.split(pattern, text)
    
    # Initialiser un dictionnaire pour stocker les sections
    sections = {}
    
    # Ajouter la section avant le premier titre ( qui est introduction )
    # le texte avant va correspondre au titre de larticles, les auteurs et le resumé
    if parts[0].strip():
        sections['avant introduction'] = parts[0].strip()
    else:
        sections['avant introduction'] = ""
    
    # Parcourir les parties divisées
    current_title = None
    for part in parts[1:]:
        part = part.strip()  # Supprimer les espaces blancs en début et fin de chaîne
        if part in all_titles:
            # Trouver le titre principal correspondant
            current_title = next(key for key, variants in title_dict.items() if part in variants)
            sections[current_title] = ""
        elif current_title:
            sections[current_title] += part + " "
    
    # Supprimer les espaces blancs en fin de section
    for title in sections:
        sections[title] = sections[title].strip()
    
    # Si moins de 2 titres, faire le chunking par caractères (articles avec des titres non usuels)
    if len(sections) <= 2:
        return split_text(text)  # Par exemple, des chunks de 1000 caractères
    
    return sections


############################# deviser en chunks  ####################################

def split_text(text):
    document = Document(page_content=text)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4",
        chunk_size=1500,
        chunk_overlap=10,
    )
    chunks = text_splitter.split_documents([document])  # Passer une liste contenant le document
  
    return chunks


def extract_sections_from_texts(processed_docs, title_dict):
    """Extrait les sections de chaque texte dans une liste de textes."""
    all_sections = []
    
     
    for doc in processed_docs:
        text = doc['text']  # Extraire le texte du dictionnaire
        sections = extract_sections(text, title_dict)
        all_sections.append({
            'filename': doc['filename'],
            'sections': sections
        })
    
    return all_sections

    title_dict = {
    "Introduction": ["INTRODUCTION","Introduction", "BACKGROUND", "BACKGROUND INFORMATION","Background"],
    "Materials and Methods": ["MATERIALS AND METHODS", "METHODS","Methods" "Materials and methods","Materials and Methods"],
    "Results": ["RESULTS", "Results"],#,"Case report" pour le doc 8
    "Discussion": ["DISCUSSION", "Discussion"],
    "conclusion":["conclusion","Conclusion","CONCLUSION"]
}
'''
