import json
from copy import copy, deepcopy
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
                    print('horizontal win', i, j)
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
                    print('vert win', i, j)
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
                    print('found win')
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
                    print('found win')
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
                    print('found win')
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
                    print('found win')
                    wins = wins + 1
                    break
            else:
                currentRun = 0
            k = k + 1
            j = j - 1

    return wins, maxRun


def evalauteState(board, move, target=6):

    x,y = checkHorizontal(board, move, target) 
    x1,y1 = checkVertical(board, move, target) 
    x2,y2 =  checkDiagonal(board, move, target)
    
    
    tot_y = (y if y>1 else 0 ) + (y1 if y1>1 else 0 )+ (y2 if y2>1 else 0 )
    return  x+x1+x2, tot_y 

def getNextBestMove(Board, move):
    takenSqaures=[]
    for i in range(len(Board)):
        for j in range(len(Board[i])) :
            if(Board[i][j] != '-'):
                takenSqaures.append([i,j])
    moves =[]
    for square in takenSqaures: 
        i = square[0]
        j = square[1]
        moves.append(  list(miniMax(i,j,True, 0,0,Board,move)))
    return moves

def getEmptyAdjacentSqaures(i,j,Board):
    emptySpaces = []

    for x in [i-1, i+1]:        
        if(x < len(Board) and x >= 0):
            for y in [j-1, j+1]:
                if(y < len(Board) and y >= 0):
                    if Board[x][y] == '-':
                        emptySpaces.append([x,y])
    return emptySpaces


def miniMaxHelper(i,j,isMax, currentDepth ,maxDepth,Board, move):
    
    board = deepcopy(Board)
    board[i][j] = move
    
    if move == 'X':
        nextMove = 'Y'
    else:
        nextMove = 'X'

    if(currentDepth < maxDepth) :
        wins1, maxRun1  = evalauteState(board, move) 
        if(wins1 > 0 ) :
            return wins1 , maxRun1 , currentDepth ,i,j
        wins2, maxRun2, depth   = miniMax(i,j, not isMax , currentDepth + 1 ,maxDepth,board, nextMove)
        return wins1 + wins2, maxRun1 + maxRun2 , currentDepth  , i, j
    else:
        wins1, maxRun1 = evalauteState(board, move)
        return  wins1, maxRun1, currentDepth , i, j
def miniMax(i,j,isMax, currentDepth ,maxDepth,Board, move):
    try:
        emptySpaces = getEmptyAdjacentSqaures(i,j, Board)
        if len(emptySpaces) != 0:
            if isMax :
                values = []
                for space in emptySpaces :
                    values.append(miniMaxHelper(space[0],space[1], isMax, currentDepth ,maxDepth,Board, move))
                maxValue =  max( values ) 
                return maxValue
            else:
                values = []
                for space in emptySpaces :
                    values.append(miniMaxHelper(space[0],space[1], isMax, currentDepth ,maxDepth,Board, move))
                minValue =  min( values ) 
                return minValue
        else:
            return 0,0
            
    except Exception as e:
        print(e, emptySpaces)