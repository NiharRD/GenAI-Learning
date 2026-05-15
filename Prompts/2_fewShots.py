# Few Shots Prompting 

from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

## Few Shots Prompting:  Providing the model with a few examples of the task you want it to perform, 
# along with instructions.
SYSTEM_PROMPT = """
You are an expert in Maths and only and only ans maths realted questions.

OutputFormat : {"answer": "string" or NULL , "isCodingQuestion" : true or false }

Example 1:
Question: What is 2 + 2?
Answer:  {"answer": "4", "isCodingQuestion": false}
Example 2:
Question: Write a python code to print hello world?
Answer: {"answer": "print('Hello, World!')", "isCodingQuestion": true}  
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Give me rust code to print hello world in js  "}
    ]
)

print(response.choices[0].message.content)