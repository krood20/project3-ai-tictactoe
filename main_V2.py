import json
from copy import copy, deepcopy
import math
import http.client
import api_interaction as API
import time
import naveed_ai as AI
import alphaBetaPruning_V6 as ABP


conn = http.client.HTTPSConnection("www.notexponential.com")
payload = ''
headers = {
  'x-api-key': '49d038fb3c2011271e31',
  'userId': '1071'
}
#"2577"
gameId = input("Enter GameID:")
teamId = '1260'
#target
target = int(input("Target length:"))

while True :
    #getting moves'
    time.sleep(1)
    moves = API.get_moves(conn, payload, headers, gameId,'1')
    print(moves)
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
    #for row in board:
    #    print(row)
        
    result = ABP.checkForWin(board, len(board), target)
    if result != None:
        if result == 'X':
            print('X wins')
        elif result == 'O':
            print('O wins')
        elif result == '-':
            print('Tie')
    
    ABP.drawBoard(board)
    move = ABP.getNextBestMove(board, move, target)
    move = str(move[0]) + ',' + str(move[1])
    print(move)
    ## re establishing connection
    conn = http.client.HTTPSConnection("www.notexponential.com")
    API.make_move(conn, payload, headers,teamId, move, gameId)