import json
from copy import copy, deepcopy
import math
import http.client
import api_interaction as API
import time
# AI functions


def boardStringTo2DArray(boardString):

    rows = boardString.split("\n")
    n = len(rows[0])
    board = [['-' for i in range(n)] for j in range(n)]
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            board[i][j] = cell
    return board


def checkForDraw(board):
    for row in board:
        for item in row:
            if(item == ' '):
                return False
    return True


def checkHorizontal(board, move, target=6):
    maxRun = 0
    for i in range(len(board)):
        currentRun = 0
        for j in range(len(board)):
            if(board[i][j] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    #print('horizontal win', i, j)
                    return 1, maxRun
            else:
                currentRun = 0
    return 0, maxRun


def checkVertical(board, move, target=6):
    maxRun = 0
    for i in range(len(board)):
        currentRun = 0

        for j in range(len(board)):
            if(board[j][i] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    #print('vert win', i, j)
                    return 1, maxRun
            else:
                currentRun = 0

    return 0, maxRun


def checkDiagonal(board, move, target=6):
    n = len(board)
    wins = 0
    maxRun = 0
    for i in range(n - target + 1):
        k = 0
        j = i
        currentRun = 0
        while k <= n-1 and j <= n-1:

            if(board[k][j] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    wins = wins + 1
                    break
            else:
                currentRun = 0
            k = k + 1
            j = j + 1

        k = len(board) - 1
        j = i
        currentRun = 0
        while k >= 0 and j <= n-1:
            if(board[k][j] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    wins = wins + 1
                    break
            else:
                currentRun = 0
            k = k - 1
            j = j + 1

    for i in range(1, n - target + 1):
        k = 0
        j = i
        currentRun = 0
        while k <= n-1 and j <= n - 1:
            if(board[j][k] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    wins = wins + 1
                    break
            else:
                currentRun = 0
            k = k + 1
            j = j + 1

        k = 0
        j = n - i - 1
        currentRun = 0
        while k <= n - 1 and j <= n - 1:
            if(board[j][k] == move):
                currentRun = currentRun + 1
                if(currentRun > maxRun):
                    maxRun = currentRun
                if currentRun == target:
                    wins = wins + 1
                    break
            else:
                currentRun = 0
            k = k + 1
            j = j - 1

    return wins, maxRun


def checkForWins(board, move, target=6):
    x, y = checkHorizontal(board, move, target)
    x1, y1 = checkVertical(board, move, target)
    x2, y2 = checkDiagonal(board, move, target)
    return max([x, x1, x2])


def evalauteState(board, move, target=6):

    # finding wins
    x, y = checkHorizontal(board, move, target)
    x1, y1 = checkVertical(board, move, target)
    x2, y2 = checkDiagonal(board, move, target)

    if(move == 'X'):
        opMove = 'O'
    else:
        opMove = 'X'
    # findingLoses
    a, b = checkHorizontal(board, opMove, target)
    a1, b1 = checkVertical(board, opMove, target)
    a2, b2 = checkDiagonal(board, opMove, target)

    return (x + x1 + x2) - (a + a1 + a2), max([b, b1, b2])


def getBestScoringMove(moves):
    moves  = filter(lambda x: x is not None , moves) 
    bestMove = [0, 0, 0, 0, 0]
    for move in moves:
        if move[0] > bestMove[0]:
            bestMove = move
        elif move[0] == bestMove[0]:
            if move[1] > bestMove[1]:
                bestMove = move
    return bestMove


def getWorstScoringMove(moves):
    moves  = filter(lambda x: x is not None , moves) 
    bestMove = [math.inf, math.inf, math.inf, 0, 0]
    for move in moves:
        if move[0] < bestMove[0]:
            bestMove = move
        elif move[0] == bestMove[0]:
            if move[1] < bestMove[1]:
                bestMove = move
    return bestMove


def getNextBestMove(Board, move):

    potentialMoveSqaures = []
    for i in range(len(Board)):
        for j in range(len(Board[i])):
            if(Board[i][j] != '-'):
                potentialMoveSqaures.append([i, j])
    if len(potentialMoveSqaures) > 0:
        moves = []
        for square in potentialMoveSqaures:
            i = square[0]
            j = square[1]
            moves.append(miniMax(i, j, True, 0, 2, Board, move, move))

        bestMove = getBestScoringMove(moves)
        return [bestMove[3], bestMove[4]]
    else:
        return [math.trunc(len(Board) / 2), math.trunc(len(Board) / 2)]


def getEmptyAdjacentSqaures(i, j, Board):
    emptySpaces = []

    for x in [i-1, i, i+1]:
        if(x < len(Board) and x >= 0):
            for y in [j-1, j, j+1]:
                if(y < len(Board) and y >= 0 and (x != i or y != j)):
                    if Board[x][y] == '-':
                        emptySpaces.append([x, y])
    return emptySpaces


def miniMaxHelper(i, j, isMax, currentDepth, maxDepth, Board, move, originalMove):
    board = deepcopy(Board)
    board[i][j] = move
    if move == 'X':
        nextMove = 'O'
    else:
        nextMove = 'X'
    if(currentDepth < maxDepth):
        return miniMax(i, j, not isMax, currentDepth + 1, maxDepth, board, nextMove , originalMove)
    else:
        wins1, maxRun1 = evalauteState(board, originalMove)
        return [wins1, maxRun1, currentDepth, i, j]


def miniMax(i, j, isMax, currentDepth, maxDepth, Board, move, originalMove):
    emptySpaces = getEmptyAdjacentSqaures(i, j, Board)
    if len(emptySpaces) != 0:
        if isMax:
            values = []
            for space in emptySpaces:
                values.append(miniMaxHelper(space[0], space[1], isMax, currentDepth, maxDepth, Board, move, originalMove))
                maxValue = getBestScoringMove(values)
            return maxValue
        else:
            values = []
            for space in emptySpaces:
                values.append(miniMaxHelper(space[0], space[1], isMax, currentDepth, maxDepth, Board, move, originalMove))
            minValue = getWorstScoringMove(values)
            return minValue
    else:
        if(currentDepth > 0):
            wins1, maxRun1 = evalauteState(Board, originalMove)
            return [wins1, maxRun1, currentDepth, i, j]
        else:
           return [-math.inf, -math.inf, -math.inf, 0, 0]


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
    boardString =  json.loads(boardString)
    boardString = boardString["output"]
    board = boardStringTo2DArray(boardString)
    for row in board:
        print(row)
    move = getNextBestMove(board, move)
    move = str(move[0]) + ',' + str(move[1])
    API.make_move(conn, payload, headers,timeId, move, gameId)


    