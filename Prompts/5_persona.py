# Persona-based prompting is a technique in prompt engineering where you instruct an AI to adopt a specific identity, profession, or character before it completes a task.

# Instead of just asking the AI a question, you first tell it who it is. By putting
#  the AI into a specific "role," 
# you change the lens through which it interprets your request,
#  heavily influencing the tone, vocabulary, formatting, and depth of the response

from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT =  """"
Act as a senior marketing copywriter [Persona]. Write an email campaign 
[Task] aimed at Gen Z college students [Audience]. Keep the tone punchy
 and limit it to 100 words [Format]
"""
input_line=input("Enter your query: ")
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": input_line }
    ]
)

print(response.choices[0].message.content)