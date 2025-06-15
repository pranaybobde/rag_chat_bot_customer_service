import uvicorn
from chatbot import Chatbot
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGING_FACE_TOEKEN = os.getenv("HUGGING_FACE_TOEKEN")

from huggingface_hub import login
login(HUGGING_FACE_TOEKEN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session = Chatbot(api_key=GROQ_API_KEY)
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=".", html=True), name="static")

class UserInput(BaseModel):
    message: str

@app.post("/chat/")
def chat(user_input: UserInput):
    try:
        response = app.state.session.handle_input(user_input.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)




# Hardcoded questions

# query_1 = "I want to file a complaint about a delivered food."
# print(f"User: {query_1}")
# print("Bot:", session.handle_input(query_1))

# query_2 = "Ibon Leo"
# print(f"User: {query_2}")
# print("Bot:", session.handle_input(query_2))

# query_3 = "7777777777"
# print(f"User: {query_3}")
# print("Bot:", session.handle_input(query_3))

# query_4 = "777@gmail.com"
# print(f"User: {query_4}")
# print("Bot:", session.handle_input(query_4))

# query_5 = "I got burnt fried rice."
# print(f"User: {query_5}")
# print("Bot:", session.handle_input(query_5))

# query_6 = "Tell me the status of complaint id bb0fea97-2bdf-429a-9ad2-60ef54ddcfc6."
# print(session.handle_input(query_6))
# print(f"User: {query_6}")
