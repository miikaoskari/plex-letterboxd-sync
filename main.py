from fastapi import FastAPI
from sync import start_sync

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def start_sync():
    start_sync()
    return {"message": "Starting sync"}