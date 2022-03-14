import asyncio
import json
import uuid
from fastapi import FastAPI, WebSocket, Request, Response, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from player import Player
from game import Game
import time

games = {}
ws_message = {'type': None,
              'data': None}

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
favicon_path = 'ship.ico'
templates = Jinja2Templates(directory="templates")

@app.get('/ship.ico')
async def favicon():
    return FileResponse(favicon_path)

@app.get('/', response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.get('/create_game', response_class=HTMLResponse)
async def game(request:Request):
    return templates.TemplateResponse('game.html', {"request": request, 'socket': 'host', 'gameid': ''})

@app.get('/connect_game', response_class=HTMLResponse)
async def game(request:Request):
    game_id = request.query_params['codetext']
    return templates.TemplateResponse('game.html', {"request": request, 'socket': 'client', 'gameid': game_id})

@app.get('/checkgame')
async def checkgame(request:Request, response:Response):
    print(request.query_params)
    game_id = request.query_params['codetext']
    if game_id in games.keys():
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.websocket("/host")
async def host(websocket: WebSocket):
    await websocket.accept()
    player = Player()
    player.ws = websocket
    game = Game()
    game.players.append(player)
    game_uuid = uuid.uuid4().hex[:8]
    ws_message['type'] = 'id'
    ws_message['data'] = game_uuid
    await websocket.send_json(ws_message)
    games[game_uuid] = game
    while len(game.players) < 2:
        await asyncio.sleep(0.1)
    ws_message['type'] = 'service'
    ws_message['data'] = 'new_player'
    await websocket.send_json(ws_message)
    try:
        message = await websocket.receive_json()
        if message['type'] == 'ready':
            player.field = message['data']
            player.ready = True
        while not game.players[1].ready:
            await asyncio.sleep(0.1)
        ws_message['type'] = 'ready'
        print('host')
        await websocket.send_json(ws_message)
        while True:
            message = await websocket.receive_json()
            if message['type'] == 'shoot':
                game.buffer = message['data']
            while game.buffer != -2:
                await asyncio.sleep(0.1)
            i = game.buffer // 10
            j = game.buffer % 10
            ws_message['type'] = 'shoot'
            if player.field[i][j]:
                ws_message['data'] = 1
            else:
                ws_message['data'] = 0
            game.buffer = -1
            await websocket.send_json(ws_message)
            
    except WebSocketDisconnect:
        print('Host sbejal')
        ws_message['type'] = 'offline'
        await game.players[1].ws.send_json(ws_message)


@app.websocket("/client/{codetext}")
async def client(websocket: WebSocket, codetext:str):
    await websocket.accept()
    print(codetext)
    player = Player()
    player.ws = websocket
    game = games[codetext]
    game.players.append(player)
    try:
        message = await websocket.receive_json()
        if message['type'] == 'ready':
            player.field = message['data']
            player.ready = True
        while not game.players[0].ready:
            await asyncio.sleep(0.1)
        ws_message['type'] = 'ready'
        print('client')
        await websocket.send_json(ws_message)
        while True:
            while game.buffer != -1:
                await asyncio.sleep(0.1)
            i = game.buffer // 10
            j = game.buffer % 10
            ws_message['type'] = 'shoot'
            if player.field[i][j]:
                ws_message['data'] = 1
            else:
                ws_message['data'] = 0
            game.buffer = -2
            await websocket.send_json(ws_message)
            message = await websocket.receive_json()
            if message['type'] == 'shoot':
                game.buffer = message['data']
    except Exception as e:  #WebSocketDisconnect:
        print(e, 'Otvalilsya')
        ws_message['type'] = 'offline'
        await game.players[0].ws.send_json(ws_message)
