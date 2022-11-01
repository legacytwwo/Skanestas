from app import app
from time import sleep
from random import random
from pydantic import BaseModel
from fastapi import WebSocket, BackgroundTasks

items = {}

class TickersResponse(BaseModel):
    response: list[str]

def change_price():
    while True:
        sleep(1)
        for i in list(items.keys()):
            items[i].append(items[i][-1] + generate_movement())

def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def generate_tickers():
    for i in range(100):
        if i >= 10:
            items[f'ticker_{i}'] = [0]
        else:
            items[f'ticker_0{i}'] = [0]

@app.get("/api/tickers", response_model=TickersResponse)
async def route_get_tickers(background_tasks: BackgroundTasks):
    if not items:
        generate_tickers()
        background_tasks.add_task(change_price)
    return TickersResponse(response=list(items.keys()))

@app.websocket("/api/service")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                await websocket.send_json({'data': items[data]})
            else:
                websocket.close()
                break
            sleep(1)
    except Exception as err:
        print(f'close connection with state: {err}')