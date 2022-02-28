import uuid
from fastapi import FastAPI, WebSocket, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from player import Player
from game import Game

games = {}

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
    print(game_uuid)
    games[game_uuid] = game
    while True:
        data = await websocket.receive_text()
        player2 = game.players[1]
        await player2.ws.send_text(f"Message text was: {data}")

@app.websocket("/client/{codetext}")
async def client(websocket: WebSocket, codetext:str):
    await websocket.accept()
    print(codetext)
    player = Player()
    player.ws = websocket
    game = games[codetext]
    game.players.append(player)
    while True:
        data = await websocket.receive_text()
        player1 = game.players[0]
        await player1.ws.send_text(f"Message text was: {data}")

