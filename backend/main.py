from fastapi import FastAPI
from typing import Dict
import openai
from meilisearch import Client
from fastapi.staticfiles import StaticFiles
import time
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()  
BUCKET_NAME = os.getenv("BUCKET_NAME")
URL = os.getenv("URL")
MEILISEARCH_KEY = os.getenv("MEILISEARCH_KEY")
openai.api_key = os.getenv("OPENAI_KEY")

ROOT = Path(__file__).parent.parent


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


async def get_embedding(text_to_embed):
    response = openai.Embedding.create(
        model= "text-embedding-ada-002",
        input=[text_to_embed]
    )
    embedding = response["data"][0]["embedding"]
    
    return embedding


async def run_search_question(question):
    client = Client(URL, MEILISEARCH_KEY)
    index = client.index('json_files')

    # Initialize the variable to store the question's embedding
    question_embedding = None

    words = question.split(" ")

    if len(words) <= 2:
        results = index.search(question)

        if len(results['hits']) == 0:
            retry = True
            while retry:
                try:
                    question_embedding = await get_embedding(question)
                    retry = False
                except:
                    print(f"Rate limit hit, waiting for 5 seconds before retrying...")
                    time.sleep(5)
            results = index.search(question, opt_params={"vector": question_embedding})

    else:
        # Question has more than 2 words

        retry = True
        while retry:
            try:
                question_embedding = await get_embedding(question)
                retry = False
            except: 
                print(f"Rate limit hit, waiting for 5 seconds before retrying...")
                time.sleep(5)

        # Get the results from the embeddings
        results = index.search(question, opt_params={"vector": question_embedding})

    return results

...

@app.post("/search")
async def search_engine(query: Dict[str, str]):
    question = query.get("question")

    search_results = await run_search_question(question)

    for hit in search_results['hits']:
        hit.pop('_vectors', None)
    search_results.pop('extra', None)
    
    return {"search_results": search_results} # return your result

app.mount("", StaticFiles(directory=str(ROOT / "backend/ui"), html=True), name="ui")

