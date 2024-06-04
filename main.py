from fastapi import FastAPI, WebSocket
from sync import start_sync, start_sync_daemon

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "start_sync":
            await start_sync(websocket.send_text)
