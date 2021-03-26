import json
from copy import copy, deepcopy
import math
import http.client
import api_interaction as API
import time
import naveed_ai as AI




conn = http.client.HTTPSConnection("www.notexponential.com")
payload = ''
headers = {
  'x-api-key': '49d038fb3c2011271e31',
  'userId': '1071'
}
gameId = "2170"
teamId = '1260'
target = 6


while True :
    #getting moves'
    time.sleep(.5)
    moves = API.get_moves(conn, payload, headers, gameId,'1')
    
    res =  moves.find('No moves')
    symbol= 'X'
    if(res == -1):
        moves=json.loads(moves)
        symbol = moves['moves'][0]['symbol']
    if symbol == 'X':
        move = 'O'
    else:
        move = 'X'
    ## put call to ai logic
    boardString =  API.get_board_string(conn, payload, headers, gameId)

    boardString =  json.loads(boardString)
    boardString = boardString["output"]
    board = AI.boardStringTo2DArray(boardString)
    for row in board:
        print(row)
    move = AI.getNextBestMove(board, move, target)
    move = str(move[0]) + ',' + str(move[1])
    API.make_move(conn, payload, headers,teamId, move, gameId)