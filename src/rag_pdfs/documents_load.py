from langchain_community.document_loaders import DirectoryLoader
import re
import os
import fitz  # pip install pymupdf

################## nettoyer le texte pdf #######################################"

def clean_text(text):
    """Nettoie le texte en supprimant les caractères spéciaux et en corrigeant le formatage."""
    # Remplacer les caractères indésirables par un espace
    cleaned_text = re.sub(r'[^\w\s,.!?;:()-]', ' ', text)
    # # Remplacer les espaces multiples par un seul espace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()  # Supprime les espaces au début et à la fin
  
######################### extraire un texte clean sans inlure les references + en tete + pied de page ##################################""

def extract_clean_text(pdf_path, exclude_header_footer=True):
    """Extrait et nettoie le texte d'un PDF, en retournant le texte avec les métadonnées."""
    full_text = []

    # Ouvrir le document PDF
    with fitz.open(pdf_path) as pdf:
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            text = ""

            if exclude_header_footer:
                rect = page.rect
                # Définir une zone d'extraction excluant l'en-tête et le pied de page
                clip = fitz.Rect(rect.x0, rect.y0 + 100, rect.x1, rect.y1 - 100)
                # Extraire le texte de la zone définie
                text += page.get_text("text", clip=clip)
            else:
                # Extraire tout le texte de la page
                text = page.get_text("text")

            # Nettoyer le texte
            cleaned_text = clean_text(text)
            # Ajouter le texte nettoyé avec les métadonnées à la liste
            full_text.append((cleaned_text, pdf_path, page_number + 1))  # Ajouter le texte, la source et le numéro de page

    # Exclure les sections non désirées (comme references)
    references_start = cleaned_text.lower().find("references")
    References_start = cleaned_text.lower().find("References")
    
    if references_start != -1 and (References_start == -1 or references_start < References_start):
        cleaned_text = cleaned_text[:references_start]
    elif References_start != -1:
        cleaned_text = cleaned_text[:References_start]

    return full_text  # Retourne une liste de tuples (texte, source, page)


#################### recuperer tout les pdfs #################################################

def load_pdfs(directory_path, exclude_header_footer=True):
    """Traite tous les fichiers PDF dans un répertoire donné."""
    processed_texts = []
    
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            try:
                extracted_texts = extract_clean_text(pdf_path, exclude_header_footer)
                processed_texts.extend(extracted_texts)  # Ajoute tous les tuples à la liste

            except Exception as e:
                print(f"Erreur lors du traitement de {filename}: {str(e)}")
    
    return processed_texts  # Liste qui contient les textes des PDF avec métadonnées