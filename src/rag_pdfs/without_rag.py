from langchain.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from .config import URL

def query_without_rag(question):

    model_local = Ollama(model="mistral-ollama", base_url=URL)# or mxbai-embed-large ?
    before_rag_template = "What is {topic}"
    before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
    before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
    question = {"topic": question}
    result = before_rag_chain.invoke(question)
    return result
