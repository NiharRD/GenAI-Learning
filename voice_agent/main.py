import speech_recognition as sr ;
import asyncio
from dotenv import load_dotenv 
import os
load_dotenv() 
from openai import OpenAI ,AsyncOpenAI
from openai.helpers import LocalAudioPlayer

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in cheerfull manner with full of delight and happy",
        input=speech,
        response_format="pcm"
    )as response:
        await LocalAudioPlayer().play(response)
def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2
        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        SYSTEM_PROMPT = """"
        YOU ARE AN EXPERT ASSISTANT FOR ANSWERING USER QUERIES. YOU WILL BE GIVEN A QUERY AND YOU HAVE TO ANSWER IT IN THE BEST WAY POSSIBLE.
        AND  WHAT EVER YOU SPEAK  IT WOULD BE  CONVERTED BACK INTO AUDIO AND PLAYED BACK TO THE USER. SO MAKE SURE TO ANSWER IN A WAY THAT IT CAN BE UNDERSTOOD BY THE USER.
        """
    response=client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ] )
    
    print("Answering...",)
    print(response.choices[0].message.content)
    asyncio.run(tts(speech=response.choices[0].message.content))

main()