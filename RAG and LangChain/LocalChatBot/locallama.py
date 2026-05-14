from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

prompt=ChatPromptTemplate.from_messages( [
    ("system","You are a helpful assistant that translates ,which does not give any hallucination."),
    ("user","Questions : {questions}")
])

## Streamlit app
st.title(" App with Langchain and Local LLM")
text_input=st.text_area("Questions you want to ask:")


## OpneAI LLM
llm=Ollama(model="gemma3:1B")
output_parser=StrOutputParser()

#Langchain inference 
chain=prompt|llm|output_parser ## works as a pipeline for prompt , LLM and output parser

if text_input: 
    st.write( chain.invoke( {"questions":text_input}))
