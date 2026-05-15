from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

## Zero Shot Prompting:  Directly giving instructions to the model
## a task without giving it any examples of what a "correct" answer looks like. 
# You are essentially asking the AI to understand your instructions 
# and generate the desired output based purely on its pre-existing, 
# built-in knowledge.
SYSTEM_PROMPT = """
You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that.
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Help me write hello world in python  "}
    ]
)

print(response.choices[0].message.content)