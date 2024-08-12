from langchain.prompts import ChatPromptTemplate 
from langchain_community.chat_models import ChatOllama
from .embedding import embedding_modele
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from .config import URL

CHROMA_PATH="src/rag_pdfs/chroma"

rag_template = """Please provide a precise and well-structured answer to the following question based on the context provided without gibing references. Ensure that your response is accurate and directly addresses the question.
context : {context}
question : {question}
"""

def query_rag(question):
    embedding_f = embedding_modele()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_f)
    # rechercher dans la base de donnees
    results = db.similarity_search_with_score(question, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(rag_template)
    prompt = prompt_template.format(context=context_text, question=question)

    model_local = Ollama(model="mistral-ollama", base_url=URL)# or mxbai-embed-large ?
    response = model_local.invoke(prompt)
    sources = [doc.metadata.get("id") for doc, _score in results]
    #reponse.content pour recuperer que le texte sans les metadonnes
    #formatted_response = f"Response: {response}\n\nSources: {sources}"#source : documents_resume/doc11.txt:5:1 avec  documents_resume/doc11.txt : le chemin vers le doc, 5 : numero de la page, 1 : l'index du chunk
    
    # Retourner la réponse et les sources séparément
    return response, sources
