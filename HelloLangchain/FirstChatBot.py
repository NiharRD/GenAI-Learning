from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI ## For calling OpenAI LLM instance
from langchain_core.prompts import ChatPromptTemplate ## For creating chat prompt templates
from langchain_core.output_parsers import StrOutputParser

# # Parser  it converts LLM's response  to string , as generally LLMs return response in dict format
##  LLM Response: "Sure! Here they are: 1. Apple, 2. Banana, 3. Cherry."
## Output Parser will convert it to : "Sure! Here they are: 1. Apple, 2. Banana, 3. Cherry."


import os


os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
## Langmith tracking , MKC iski zarurat nahi hai agar aap Langsmith use nahi kar rahe hain
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

prompt=ChatPromptTemplate.from_messages( [
    ("system","You are a helpful assistant that translates ,which does not give any hallucination."),
    ("user","Questions : {questions}")
])



## OpneAI LLM
llm=ChatOpenAI(model_name="gpt-3.5-turbo")
output_parser=StrOutputParser()

#Langchain inference 
chain=prompt|llm|output_parser ## works as a pipeline for prompt , LLM and output parser

response=chain.invoke({"questions":"List of 5 fruits."})
## Invoke method is used to call the chain with input 
print(response)



