from dotenv import load_dotenv
load_dotenv()
from .server import app
import uvicorn 

def main():
    uvicorn.run(app=app,host="127.0.0.1", port=8000)

main()