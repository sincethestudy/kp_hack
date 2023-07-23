from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import time
import json

import os
import openai
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

from grid import Grid
from prompt import Prompt

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
    system_message: str
    user_message: str
    inputs: Union[str, list]


def data_streamer(data):
    for character in data:
        yield character
        time.sleep(0.01)


@app.get("/")
def read_root():
    return {"Hello": openai.Model.list()}

@app.post("/complete")
def complete(item: Item):
    system_message = item.system_message
    user_message = item.user_message
    inputs = item.inputs

    prompt = Prompt(system_message, user_message)
    grid = Grid(prompt, (2, 2))

    def data_streamer():
        for text, idx in grid.sample_one(inputs):
            yield json.dumps({'text': text, 'box_idx': idx}) + '\n'
    
    return StreamingResponse(data_streamer(), media_type="text/event-stream") # type: ignore
