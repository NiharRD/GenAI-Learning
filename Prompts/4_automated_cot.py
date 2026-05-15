
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

## Chain of Thought (CoT) prompting is a technique used to improve the reasoning capabilities 
# of Large Language Models (LLMs). Instead of asking the AI to jump straight from a question to 
# an answer, CoT forces the model to articulate its intermediate reasoning steps—much like asking
#  a human to "show their work" in a math problem.
SYSTEM_PROMPT=""""
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT", "content": "3.5" }
"""

user_input= input("Enter your query: ")

messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_input }]

while True: 

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=messages)
   # response_content = response.choices[0].message.content

    raw_content = response.choices[0].message.content
    response_data = json.loads(raw_content)

    if response_data.get("step") == "OUTPUT": 
        print("Final Output: ", response_data.get("content"))
        break
        
    elif response_data.get("step") == "PLAN":
        print("AI thinking guys: ", response_data.get("content"))
        # You can just append the raw string directly back to the message history
        messages.append({"role": "assistant", "content": raw_content})
        
    elif response_data.get("step") == "START":
        print("AI has started to solve the problem: ", response_data.get("content"))



# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         { "role": "system", "content": SYSTEM_PROMPT },
#         { "role": "user", "content": "Hey, Can you solve 2 + 3 * 5 / 10" },
      
#            { "role": "assistant", "content":  json.dumps({
#  "step": "START",
#  "content": "Hey, Can you solve 2 + 3 * 5 / 10"
# }) } , { "role": "assistant", "content":  json.dumps({"step": "PLAN", "content": "Seems like the user is asking to solve a mathematical expression. I need to apply the correct order of operations (BODMAS/PEMDAS) to get the accurate result."}) } 
#   ,{"role" :"assistant", "content": json.dumps({"step": "PLAN", "content": "According to the order of operations (BODMAS/PEMDAS), multiplication and division should be performed before addition."})  }  ]
# )   

# ## Keep appending those Hehe
# print(response.choices[0].message.content)