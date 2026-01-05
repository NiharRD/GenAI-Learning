from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
## Parser  it converts LLM's response  to string , as generally LLMs return response in dict format
##  LLM Response: "Sure! Here they are: 1. Apple, 2. Banana, 3. Cherry."
## Output Parser will convert it to : "Sure! Here they are: 1. Apple, 2. Banana, 3. Cherry."


import streamlit as st
import os


os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

prompt=ChatPromptTemplate.from_messages( [
    ("system","You are a helpful assistant that translates ,which does not give any hallucination."),
    ("user","Questions : {questions}")
])

## Streamlit app
st.title(" App with Langchain and OpenAI")
text_input=st.text_area("Questions you want to ask:")

## OpneAI LLM
llm=ChatOpenAI(model_name="gpt-3.5-turbo")
output_parser=StrOutputParser()

#Langchain inference 
chain=prompt|llm|output_parser ## works as a pipeline for prompt , LLM and output parser

if text_input: 
    st.write( chain.invoke( {"questions":text_input}))


## To run the app use : streamlit run app.py
