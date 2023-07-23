from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import time


import os
import openai
openai.organization = "org-hwLZwQZTV54TcPiMbEvqjUwo"
openai.api_key = os.getenv("OPENAI_API_KEY")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5174",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    prompt: str


def data_streamer(data):
    for character in data:
        yield character
        time.sleep(0.01)


@app.get("/")
def read_root():
    return {"Hello": openai.Model.list()}

@app.post("/complete")
def complete(item: Item):

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": item.prompt}
            ]
        ).choices[0].message.content # type: ignore
    
    print(chat_completion)

    return StreamingResponse(data_streamer(chat_completion), media_type="text/plain") # type: ignore
