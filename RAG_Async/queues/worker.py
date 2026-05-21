import os 
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

embedding_model = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small") 

vector_db= QdrantVectorStore.from_existing_collection(
    collection_name="nodejs-docs",
    url= "http://localhost:6333",
    embedding=embedding_model

)

def process_query(query:str):
    print("Searching in the chunks",query)
    search_results=vector_db.similarity_search(query=query,)
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results ])

    SystemPROMPT = f""""

You are an AI assistant for answering user queries related to NODE JS documentation. Use the following retrieved similar documents as context to answer the question.
Context: {context}
"""
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SystemPROMPT},    
        {"role": "user", "content": query}
    ]
)
    return response.choices[0].message.content