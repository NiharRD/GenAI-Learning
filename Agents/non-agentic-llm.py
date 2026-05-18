
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


input_line="What is the current time  and weather in barpeta assam as of date  ?"
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
       
        { "role": "user", "content": input_line }
    ]
)

print(response.choices[0].message.content)