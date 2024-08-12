FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
COPY src/rag_pdfs/Modelfile /Modelfile
COPY src/rag_pdfs/Modelfile.embeddings /Modelfile.embeddings
