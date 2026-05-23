from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver  

load_dotenv()

llm=ChatOpenAI(model="gpt-4o")
MONGODB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin" 
with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:


    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def chatbot(state: State):
        response = llm.invoke(state.get("messages"))
        return { "messages": [response] }
    def samplenode(state: State):
        print("\n\nInside samplenode node", state)
        return { "messages": ["Sample Message Appended"] }

    graph_builder = StateGraph(State) ## Providing initial state to the graph builder, which will be used to validate the state at each node and edge.

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("samplenode", samplenode)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", "samplenode")
    graph_builder.add_edge("samplenode", END)

    graph = graph_builder.compile(checkpointer=checkpointer)
    config = {
        "configurable": {
            "thread_id": "nihar's memory thread",
        }
    }

    # updated_state = graph.invoke(State({"messages": ["What is my name?"]}))
    # print("\n\nupdated_state", updated_state)

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": "Whats my name ?"}]},
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()






    # (START) -> chatbot -> samplenode -> (END)

    # state = { messages: ["Hey there"] }
    # node runs: chatbot(state: ["Hey There"]) -> ["Hi, This is a message from ChatBot Node"]
    # state = { "messages": ["Hey there", "Hi, This is a message from ChatBot Node"]  }
