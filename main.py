import json
from copy import copy, deepcopy
import math
import http.client
import api_interaction as API
import time

conn = http.client.HTTPSConnection("www.notexponential.com")
payload = ''
headers = {
  'x-api-key': '49d038fb3c2011271e31',
  'userId': '1071'
}
gameId = "2127"
#get_moves(conn, payload, headers, gameId, "30")



API.get_moves(conn, payload, headers, gameId,'1')
lastMove = ['6','6']

moves = API.get_moves(conn, payload, headers, gameId,'1')
moves=json.loads(moves)
x = moves['moves'][0]['moveX']
y = moves['moves'][0]['moveY']
symbol = moves['moves'][0]['symbol']
timeId = '1260'

while True :
    #getting moves'
    time.sleep(.5)
    moves = API.get_moves(conn, payload, headers, gameId,'1')
    moves=json.loads(moves)
    x = moves['moves'][0]['moveX']
    y = moves['moves'][0]['moveY']
    symbol = moves['moves'][0]['symbol']
    if symbol == 'X':
        move = 'O'
    else:
        move = 'X'
    boardString =  API.get_board_string(conn, payload, headers, gameId)
    
    # boardString =  json.loads(boardString)
    # boardString = boardString["output"]
    # board = boardStringTo2DArray(boardString)
    # for row in board:
    #     print(row)
    # move = getNextBestMove(board, move)
    # move = str(move[0]) + ',' + str(move[1])
    API.make_move(conn, payload, headers,timeId, move, gameId)