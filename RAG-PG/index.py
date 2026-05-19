from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
load_dotenv()

path= Path(__file__).parent / "nodeJS.pdf"
docs = PyPDFLoader(path).load()

## Its the  document , that we have converted into a list of documents using the PyPDFLoader
## simple list of texts

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chuncks = text_splitter.split_documents(docs)

embedding_model = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small") 
  

vector_store= QdrantVectorStore.from_documents(
    documents=chuncks,
    embedding=embedding_model,
    collection_name="nodejs-docs",
    url= "http://localhost:6333"
)