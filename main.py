from fastapi import FastAPI, WebSocket
from sync import start_sync
import logging
import asyncio
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    async def send_progress(progress):
        logging.info("Sending... %s", progress)
        await websocket.send_text(progress)
        await asyncio.sleep(0)

    while True:
        data = await websocket.receive_text()
        if data == "start_sync":
            await start_sync(send_progress)
