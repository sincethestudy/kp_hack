from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json

import os
import openai

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

from mutate import mutate_prompt
from generate import generate_parallel


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5174",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GRID_SIZE = 2*2

class GenerationItem(BaseModel):
    system_message: str
    prompts: list
    inputs: list


class MutationItem(BaseModel):
    prompt: str
    instructions: str


@app.get("/")
def read_root():
    return {"Hello": openai.Model.list()}


@app.post("/mutate")
def mutate(item: MutationItem):
    prompt = item.prompt
    instructions = item.instructions
    return mutate_prompt(prompt, instructions, n=GRID_SIZE)


@app.post("/generate")
def generate(item: GenerationItem):
    system_message = item.system_message
    prompts = item.prompts
    inputs = item.inputs

    def data_streamer():
        for text, idx in generate_parallel(system_message, inputs, prompts):
            yield json.dumps({"text": text, "box_idx": idx}) + "\n"
    
    return StreamingResponse(
        data_streamer(), media_type="text/event-stream"
    )  # type: ignore

