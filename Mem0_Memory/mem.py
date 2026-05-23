from mem0 import Memory
from dotenv import load_dotenv
load_dotenv()
import os 
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "text-embedding-3-small" }
    },
    "llm": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "gpt-4o" }
    },
   
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },"graph_store":{
        "provider": "neo4j",
        "config": {
            "url": os.getenv("Neo4j_CONNECTOR_URL"),
            "username": os.getenv("Neo4j_USERNAME"),
            "password": os.getenv("Neo4j_PASSWORD")
        }
    },
}

mem_client=Memory.from_config(config)


while True:


    user_query = input("> ")

 
    relevet_search_memory = mem_client.search(query=user_query,filters={"user_id": "niharRD"}) ## Searching for relevant memories based on the user query and user ID

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in relevet_search_memory.get("results")
    ]

    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_query }
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI:", ai_response)

    ## Appending the new memory to the vector store with user ID as filter for future retrievals. This will help in building a long-term memory for the user.
    mem_client.add(
        user_id="niharRD",
        messages=[
            { "role": "user", "content": user_query },
            { "role": "assistant", "content": ai_response }
        ]
    )

    print("Memory has been saved...")