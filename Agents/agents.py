
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import requests
from pydantic import BaseModel
from typing import Optional

load_dotenv()



class OutputFormat(BaseModel):
    step: str
    content: str
    tool: Optional[str] = None
    tool_input: Optional[dict] = None

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
def run_command(cmd: str):
    result = os.system(cmd)
    return result


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

def get_current_time(timezone: str = "Asia/Kolkata"):
    # url expects a timezone like 'Asia/Kolkata' or 'Europe/Paris'
    url = f"http://worldtimeapi.org/api/timezone/{timezone}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # The datetime format looks like '2023-10-25T14:30:00.123456+05:30'
        raw_time = data['datetime']
        clean_time = raw_time.split('T')[1].split('.')[0] 
        
        # Make the output a bit friendlier if it's the default timezone
        display_location = "India" if timezone == "Asia/Kolkata" else timezone
        return f"The current time in {display_location} is {clean_time}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "get_current_time": get_current_time , 
    "run_command": run_command
}


SYSTEM_PROMPT=""""
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call an TOOL  if required from the list of available tools.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Avaiable tools 
    1. get_weather(city: str) -> str : This tool takes city name as input and gives current weather information about that city as output.
    2. get_current_time(timezone: str) ->  str  : This tool takes timezone as input and gives current time information about that timezone as output. The timezone should be in the format like 'Asia/Kolkata' or 'Europe/Paris'
    3. run_command(cmd: str) -> str : This tool takes a command as input and runs that command in the terminal and gives the output of that command as output.
    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE", "content": "string" , "tool": "tool_name_if_step_is_TOOL", "tool_input": { tool_input_dict_if_step_is_TOOL } }

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

    Example:
    START: Hey, can you tell me the current weather in barpeta assam?
    PLAN: { "step": "PLAN", "content": "Seems like user is interested in getting current weather information" }
    PLAN: { "step": "PLAN", "content": "looking at the problem, we  can 't get correct answer from my pretrained data , so i should call an tool" }
    PLAN: { "step": "PLAN", "content": "Let me see the avaiable tools that i have access to ." }
    PLAN: { "step": "PLAN", "content": "great , we have get_weather tool available. " }
    PLAN: { "step": "PLAN", "content": "I will call the get_weather tool with the city name as input i.e Barpeta" }
    TOOL: { "step": "TOOL", "content": "calling get_weather with barpeta as input" ,"tool": "get_weather", "tool_input": {"city": "Barpeta"} }
    OBSERVE: { "step": "OBSERVE", "tool":"get_weather" , "output" : "Mist, Light Rain With Thunderstorm +25°C"   }
    PLAN: { "step": "PLAN", "content": "Great , we got the weather information for Barpeta and its 25°C with mist, light rain with thunderstorm " }
    
    OUTPUT: { "step": "OUTPUT", "content": "So the weather in Barpeta is mist, light rain with thunderstorm and the temperature is 25°C." }
"""

while True:
    user_input= input("Enter your query: ")

    messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": user_input }]

    while True: 

            response = client.chat.completions.parse(
        model="gemini-2.5-flash",
        response_format=OutputFormat,
        messages=messages)
   # response_content = response.choices[0].message.content

            raw_content = response.choices[0].message.content
            response_data = json.loads(raw_content)
            parsed_response = response.choices[0].message.parsed

            if parsed_response.step == "OUTPUT": 
                print("Final Output: ", parsed_response.content)
                break
                
            elif parsed_response.step == "PLAN":
                print("AI thinking guys: ", parsed_response.content)
                # You can just append the raw string directly back to the message history
                messages.append({"role": "assistant", "content": raw_content})
                
            elif parsed_response.step == "START":
                print("AI has started to solve the problem: ", parsed_response.content)

            elif parsed_response.step == "TOOL":
                tool_name = parsed_response.tool
                tool_input = parsed_response.tool_input
                print(f"AI is calling tool {tool_name} with input {tool_input}")
                
                # Call the appropriate tool function based on the tool name
                if tool_name in available_tools:
                    tool_function = available_tools[tool_name]
                    tool_output = tool_function(**tool_input)
                    print(f"Tool output: {tool_output}")
                    
                    # Append the observation back to the message history
                    observation_message = {
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": tool_name,
                            "output": tool_output
                        })
                    }
                    messages.append(observation_message)
                else: 
                    print(f"Subagent tried to use missing or invalid tool: {tool_name}")
                    # Append error as observation so the LLM knows it failed
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": tool_name,
                            "output": f"Error: Tool '{tool_name}' not found."
                        })
                    })



