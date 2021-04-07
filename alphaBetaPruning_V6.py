#!/usr/bin/env yPosthon3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 19:39:27 2021

@author: kingrice
"""

from itertools import groupby
import numpy as np
import math as m
import random as r
    
def createBoard(n):
    board = [['-' for col in range(n)] for row in range(n)]
    return board

def drawBoard(board):
    for row in range(len(board)):
        for col in range(len(board)):
            print('{}|'.format(board[row][col]), end=" ")      
        print()
    print()

def checkForWin(board, boardSize, winThreshold):
        
    #Vertical win
    for col in range(0,boardSize):
        test_list = [row[col] for row in board]
        listOfRuns = [(symbol, list(run)) for symbol, run in groupby(test_list)]
        longestRun = max(listOfRuns, key=lambda x:len(x[-1]))
        if len(longestRun[1]) == winThreshold and longestRun[0] != '-':
            return longestRun[0]
            
    #Horizontal win
    for row in range(0, boardSize):
        listOfRuns = [(symbol, list(run)) for symbol, run in groupby(board[row])]
        longestRun = max(listOfRuns, key=lambda x:len(x[-1]))
        if len(longestRun[1]) == winThreshold and longestRun[0] != '-':
            return longestRun[0]
        
        
    #Diagonal win
    npBoard = np.array(board)
    diags = [npBoard[::-1,:].diagonal(i) for i in range(-npBoard.shape[0]+1,npBoard.shape[1])]
    diags.extend(npBoard.diagonal(i) for i in range(npBoard.shape[1]-1,-npBoard.shape[0],-1))
    for d in diags:
        if len(d) >= winThreshold:
            listOfRuns = [(symbol, list(run)) for symbol, run in groupby(d.tolist())]
            longestRun = max(listOfRuns, key=lambda x:len(x[-1]))
            if len(longestRun[1]) == winThreshold and longestRun[0] != '-':
                return longestRun[0]
    
    #Check if board is full
    for row in range(0, boardSize):
        for col in range(0, boardSize):
            if board[row][col] == '-':
                return None
    
    return '-'

def tryMask(board, player):
    
    potMoves = []
    npBoard = np.array(board)
    oMask = np.ma.masked_where(npBoard=='O', npBoard)
    xMask = np.ma.masked_where(npBoard=='X', npBoard)
    dMask = np.ma.masked_where(npBoard=='-', npBoard)
    
    #print(xMask)
    #get the moves immediately arround the vicinity of placed elements
    if not all(board[row][col] == '-' for row in range(len(board)) for col in range(len(board))):
        if player =='X':
            #print(xMask)
            #print(oMask)
            availableMoves = np.logical_and(np.logical_not(oMask.mask), dMask.mask)
            
            aRow, aCol = np.where(availableMoves==True)
            aLocs = np.column_stack((aRow, aCol))
            
            if type(xMask.mask) != np.bool_:
                pRow, pCol = np.where(xMask.mask==True)
                pLocs = np.column_stack((pRow, pCol))
                
                for pLoc in pLocs:
                    for aLoc in aLocs:
                        dist = m.sqrt((abs(pLoc[0] - aLoc[0]))**2 + (abs(pLoc[1] - aLoc[1]))**2)
                        if dist == 1 or dist == m.sqrt(2):
                            potMoves.append(aLoc.tolist())
                    
            else:
                potMoves = aLocs.tolist()
                #print('potMoves: ')
                #print(potMoves)
                
            potMoves = np.unique(potMoves, axis = 0)
            r.shuffle(potMoves)
            return potMoves
                    
        elif player =='O':
            availableMoves = np.logical_and(np.logical_not(xMask.mask), dMask.mask)
            aRow, aCol = np.where(availableMoves==True)
            aLocs = np.column_stack((aRow, aCol))
            
            if type(oMask.mask) != np.bool_:
                #print(oMask.mask)
                #print(xMask)
                pRow, pCol = np.where(oMask.mask==True)
                pLocs = np.column_stack((pRow, pCol))
            
            
            
                for pLoc in pLocs:
                    for aLoc in aLocs:
                        dist = m.sqrt((abs(pLoc[0] - aLoc[0]))**2 + (abs(pLoc[1] - aLoc[1]))**2)
                        if dist == 1 or dist == m.sqrt(2):
                            potMoves.append(aLoc.tolist())
                        
            else:
                potMoves = aLocs.tolist()
                #print('potMoves: ')
                #print(potMoves)
                
            
            potMoves = np.unique(potMoves, axis = 0)
            r.shuffle(potMoves)
            return potMoves
    
    return potMoves  

def pickFirstMove(board, boardSize, oppPlayer):
    
    #We want to avoid the edges
    bestFirstMoves = []
    cornerMoves = []
    centerMoves = []
    cornerMoves.append([0,0])
    cornerMoves.append([0,boardSize-1])
    cornerMoves.append([boardSize-1,0])
    cornerMoves.append([boardSize-1,boardSize-1])
    if boardSize % 2 == 0:
        centerMoves.append([int(boardSize/2),int(boardSize/2)])
        centerMoves.append([int(boardSize/2),int((boardSize/2) - 1)])
        centerMoves.append([int((boardSize/2)-1),int(boardSize/2)])
        centerMoves.append([int((boardSize/2)-1),int((boardSize/2)-1)])
    else:
        centerMoves.append([int(m.floor(boardSize/2)),int(m.floor(boardSize/2))])
    
    #Check if board is empty
    if all(board[row][col] == '-' for row in range(boardSize) for col in range(boardSize)):
        bestFirstMoves = cornerMoves + centerMoves
        return bestFirstMoves
    else:
        npBoard = np.array(board)
        row, col = np.where(npBoard == oppPlayer)
        if len(row) == 1:
            if [row[0],col[0]] in cornerMoves:
                return centerMoves
            else:
                return cornerMoves
        
    return bestFirstMoves

def getMove(board, player, boardSize, winThreshold):
    
    if player == 'X':
    
        xMoves = tryMask(board, 'X')
        oMoves = tryMask(board, 'O')
        (offensiveMoves, maxRunX) = selectMove(board, 'X', boardSize, winThreshold)
        (defensiveMoves, maxRunO) = selectMove(board, 'O', boardSize, winThreshold)
        
        #print('X')
        #print('xMoves: ')
        #print(xMoves)
        #print('oMoves: ')
        #print(oMoves)
        #print(offensiveMoves)
        #print(defensiveMoves)
        #if offensiveMoves and defensiveMoves:
        if offensiveMoves and defensiveMoves:
            if len(maxRunX) >= len(maxRunO):
                r.shuffle(offensiveMoves)
                move = offensiveMoves[0]
                return move
                #for move in offensiveMoves:
                #    for xlocs in xMoves:
                #        if move[0] == xlocs[0] and move[1] == xlocs[1]:
                #            return move
        
            elif len(maxRunX) < len(maxRunO):
                r.shuffle(defensiveMoves)
                move = defensiveMoves[0]
                return move
                #for move in defensiveMoves:
                #    for olocs in oMoves:
                #        if move[0] == olocs[0] and move[1] == olocs[1]:
                #            return move
        
        elif offensiveMoves:
            r.shuffle(offensiveMoves)
            move = offensiveMoves[0]
            return move
            #for move in offensiveMoves:
            #    for xlocs in xMoves:
            #        if move[0] == xlocs[0] and move[1] == xlocs[1]:
            #            return move
        
        elif defensiveMoves:
            r.shuffle(defensiveMoves)
            move = defensiveMoves[0]
            return move
            #for move in defensiveMoves:
            #    for olocs in oMoves:
            #        if move[0] == olocs[0] and move[1] == olocs[1]:
            #            return move
        
        r.shuffle(xMoves)
        return xMoves[0]
    
    else:
    
        oMoves = tryMask(board, 'O')
        xMoves = tryMask(board, 'X')
        (offensiveMoves, maxRunO) = selectMove(board, 'O', boardSize, winThreshold)
        (defensiveMoves, maxRunX) = selectMove(board, 'X', boardSize, winThreshold)
        
        #print('O')
        #print('oMoves: ')
        #print(oMoves)
        #print('xMoves: ')  
        #print(xMoves)
        #print(offensiveMoves)
        #print(defensiveMoves)
        #if offensiveMoves and defensiveMoves:
        if offensiveMoves and defensiveMoves:
            if len(maxRunO) >= len(maxRunX):
                r.shuffle(offensiveMoves)
                move = offensiveMoves[0]
                return move
                #for move in offensiveMoves:
                #    for olocs in oMoves:
                #        if move[0] == olocs[0] and move[1] == olocs[1]:
                #            return move
        
            elif len(maxRunO) < len(maxRunX):
                r.shuffle(defensiveMoves)
                move = defensiveMoves[0]
                return move
                #for move in defensiveMoves:
                #    for xlocs in xMoves:
                 #       if move[0] == xlocs[0] and move[1] == xlocs[1]:
                 #           return move
        
        elif offensiveMoves:
            r.shuffle(offensiveMoves)
            move = offensiveMoves[0]
            return move
            #for move in offensiveMoves:
            #    for olocs in oMoves:
            #        if move[0] == olocs[0] and move[1] == olocs[1]:
            #            return move
        elif defensiveMoves:
            r.shuffle(defensiveMoves)
            move = defensiveMoves[0]
            return move
            #for move in defensiveMoves:
            #    for xlocs in xMoves:
            #        if move[0] == xlocs[0] and move[1] == xlocs[1]:
            #            return move
        
        r.shuffle(oMoves)
        return oMoves[0]

   
def selectMove(board, oppPlayer, boardSize, winThreshold):
   
    #Cutoff opponent's vertical run
    maxRun = []
    startCol = None
    endCol = None
    startRow = None
    endRow = None
    orientation = None
    
    for col in range(0,boardSize):
        colList = [row[col] for row in board]
        listOfRuns = [(symbol, list(run)) for symbol, run in groupby(colList)]
        for i in range(len(listOfRuns)):
            if (listOfRuns[i][0] == oppPlayer and (len(listOfRuns[i][1]) > 1 
                and len(listOfRuns[i][1]) >= len(maxRun))):

                considerMax = False
                if len(listOfRuns) > 2 and (i > 0 and i < len(listOfRuns) - 1):
                    if listOfRuns[i-1][0] == '-' or listOfRuns[i+1][0] == '-':
                        considerMax = True
                 
                elif len(listOfRuns) > 1 and i == 0:
                    if listOfRuns[i+1][0] == '-':
                        considerMax = True
                 
                elif len(listOfRuns) > 1 and i > 0:
                    if listOfRuns[i-1][0] == '-':
                        considerMax = True
                
                if considerMax:   
            
                    #print(maxRun)
                    maxRun = listOfRuns[i][1]
                    orientation = 0
                    startCol = col
                    endCol = col
                    
                    findCounter = 0
                    runNotFound = True
                    startRow = findCounter
                    endRow = findCounter
                    while runNotFound:
                        runInfo = listOfRuns[findCounter]
                        run = runInfo[1]
                        if run != maxRun:
                            startRow = startRow + len(run)
                            findCounter = findCounter + 1
                        else:
                            endRow = startRow + len(run) - 1
                            runNotFound = False
    
    #Cutoff opponent's horizontal run
    for row in range(0,boardSize):
        listOfRuns = [(symbol, list(run)) for symbol, run in groupby(board[row])]
        for i in range(len(listOfRuns)):
            if (listOfRuns[i][0] == oppPlayer and (len(listOfRuns[i][1]) > 1 
                and len(listOfRuns[i][1]) >= len(maxRun))):
                
                considerMax = False
                if len(listOfRuns) > 2 and (i > 0 and i < len(listOfRuns) - 1):
                    if listOfRuns[i-1][0] == '-' or listOfRuns[i+1][0] == '-':
                        considerMax = True
                 
                elif len(listOfRuns) > 1 and i == 0:
                    if listOfRuns[i+1][0] == '-':
                        considerMax = True
                 
                elif len(listOfRuns) > 1 and i > 0:
                    if listOfRuns[i-1][0] == '-':
                        considerMax = True
                
                if considerMax:
                    maxRun = listOfRuns[i][1]
                    orientation = 1
                    startRow = row
                    endRow = row
                    
                    findCounter = 0
                    startCol = findCounter
                    endCol = findCounter
                    
                    runNotFound = True
                    while runNotFound:
                        runInfo = listOfRuns[findCounter]
                        run = runInfo[1]
                        if run != maxRun:
                            startCol = startCol + len(run)
                            findCounter = findCounter + 1
                        else:
                            endCol = startCol + len(run) - 1
                            runNotFound = False
    #Diagonal win
    iMask = [[[row, col] for col in range(boardSize)] for row in range(boardSize)]
    npMask = np.array(iMask)
    npBoard = np.array(board)
    
    diagsIdx = [npMask[::-1,:].diagonal(i) for i in range(-npMask.shape[0]+1,npMask.shape[1])]
    diagsIdx.extend(npMask.diagonal(i) for i in range(npMask.shape[1]-1,-npMask.shape[0],-1))
    
    diags = [npBoard[::-1,:].diagonal(i) for i in range(-npBoard.shape[0]+1,npBoard.shape[1])]
    diags.extend(npBoard.diagonal(i) for i in range(npBoard.shape[1]-1,-npBoard.shape[0],-1))
    
    for j in range(len(diags)):
        d = diags[j]
        if len(d) >= winThreshold:
            listOfRuns = [(symbol, list(run)) for symbol, run in groupby(d.tolist())]
            
            for i in range(len(listOfRuns)):
                if (listOfRuns[i][0] == oppPlayer and (len(listOfRuns[i][1]) > 1 
                    and len(listOfRuns[i][1]) >= len(maxRun))):
                    
                    considerMax = False
                    if len(listOfRuns) > 2 and (i > 0 and i < len(listOfRuns) - 1):
                        if listOfRuns[i-1][0] == '-' or listOfRuns[i+1][0] == '-':
                            considerMax = True
                     
                    elif len(listOfRuns) > 1 and i == 0:
                        if listOfRuns[i+1][0] == '-':
                            considerMax = True
                     
                    elif len(listOfRuns) > 1 and i > 0:
                        if listOfRuns[i-1][0] == '-':
                            considerMax = True
                    
                    if considerMax:   
                        maxRun = listOfRuns[i][1]
                        orientation = 2
                        findCounter = 0
                        startRow = diagsIdx[j][0][0]
                        startCol = diagsIdx[j][1][0]
                        endRow = findCounter
                        endCol = findCounter
                        runNotFound = True
                        
                        while runNotFound:
                            #print(findCounter)
                            runInfo = listOfRuns[findCounter]
                            run = runInfo[1]
                        
                            if run != maxRun:
                                if diagsIdx[j][0][0] > diagsIdx[j][0][-1]:
                                    startRow = startRow - len(run)
                                else:
                                    startRow = startRow + len(run)
                                 
                                startCol = startCol + len(run)
                                findCounter = findCounter + 1
                                
                            else:
                                if diagsIdx[j][0][0] > diagsIdx[j][0][-1]:
                                    endRow = startRow - len(run) + 1
                                else:
                                    endRow = startRow + len(run) - 1
                                 
                                endCol = startCol + len(run) - 1
                                runNotFound = False
    potMoves = []
    #print('orientation = ', orientation, 'maxRun = ', maxRun)
    #print('startCol = ', startCol, 'endCol = ', endCol, 'startRow = ', startRow, 'endRow = ', endRow)
    if orientation == 0:
        if endRow < len(board)-1 and board[endRow+1][endCol] == '-':
                potMoves.append([endRow+1, endCol])
        
        if startRow > 0 and board[startRow-1][endCol] == '-':
                potMoves.append([startRow-1, endCol])
        
    elif orientation == 1:
        if endCol < len(board)-1 and board[endRow][endCol+1] == '-':
                potMoves.append([endRow, endCol+1])
                
        if startCol > 0 and board[endRow][startCol-1] == '-':
                potMoves.append([endRow, startCol-1])
      
    elif orientation == 2:
        #if endCol > startCol and endRow > startRow:
        if endRow > startRow:
            if endCol < len(board)-1 and endRow < len(board)-1:
                if board[endRow+1][endCol+1] == '-':
                    potMoves.append([endRow+1, endCol+1])
        
            if startCol > 0 and startRow > 0: 
                if board[startRow-1][startCol-1] == '-':
                    potMoves.append([startRow-1, startCol-1])
        
        else:
            if endCol < len(board)-1 and endRow > 0:
                if board[endRow-1][endCol+1] == '-':
                    potMoves.append([endRow-1, endCol+1])
        
            if startCol > 0 and startRow < len(board) - 1: 
                if board[startRow+1][startCol-1] == '-':
                    potMoves.append([startRow+1, startCol-1])
         
        #print(potMoves)
    return (potMoves, maxRun)

def terminalTest(board, minPlayer, maxPlayer, boardSize, winThreshold):
    
    # Return Utility(state)
    winner = checkForWin(board, boardSize, winThreshold)
    if winner == minPlayer:
        return (-1, 0, 0)
    elif winner == maxPlayer:
        return (1, 0, 0)
    elif winner == '-':
        return (0, 0, 0)
    
def maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold):
    
    # depth-limited search currently not working
    # currentDepth and maxDepth are not being used
    
    value = -float("inf")
    xPos = None
    yPos = None
    
    utility = terminalTest(board, minPlayer, maxPlayer, boardSize, winThreshold)
    if utility is not None:
        return utility
    
    if currentDepth < maxDepth:
        for row in range (0,boardSize):
            for col in range (0,boardSize):
                if board[row][col] == '-':
                    board[row][col] = maxPlayer
                    (mValue, _, _) = minValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth + 1, maxDepth, boardSize, winThreshold)
            
                    if mValue > value:
                        value = mValue
                        xPos = row
                        yPos = col
                    board[row][col] = '-'
                    
                    if value >= beta:
                        return (value, xPos, yPos)
                    
                    alpha = max(alpha, value)
    
    return (value, xPos, yPos)
                
    
def minValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold):
    
    # depth-limited search currently not working
    # currentDepth and maxDepth are not being used
    
    value = float("inf")
    xPos = None
    yPos = None
    
    utility = terminalTest(board, minPlayer, maxPlayer, boardSize, winThreshold)
    if utility is not None:
        return utility
    
    if currentDepth < maxDepth:
        for row in range (0,boardSize):
            for col in range (0,boardSize):
                if board[row][col] == '-':
                    board[row][col] = minPlayer
                    (mValue, _, _) = maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth + 1, maxDepth, boardSize, winThreshold)
                    if mValue < value:
                        value = mValue
                        xPos = row
                        yPos = col 
                    board[row][col] = '-'
                    
                    if value <= alpha:
                        #print('try it')
                        return (value, xPos, yPos)
                    
                    beta = min(beta, value)
    
    return (value, xPos, yPos)

def getNextBestMove(board, player, target):
    
    maxPlayer = player
    if player == 'X':
        minPlayer = 'O'
    else:
        minPlayer = 'X'
    
    #print(maxPlayer)
    #print(target)
    
    boardSize = len(board)
    #drawBoard(board)
    winThreshold = target
    
    alpha = -float("inf")
    beta = float("inf")
    #Currently not working
    currentDepth = 0
    maxDepth = 4 
    
    if all(board[row][col] == '-' for row in range(boardSize) for col in range(boardSize)):
        #print('madeItHere')
        
        bestFirstMoves = pickFirstMove(board, boardSize, minPlayer)
        if bestFirstMoves:
            r.shuffle(bestFirstMoves)
            move = bestFirstMoves[0]
            return move
            #board[firstMove[0]][firstMove[1]] = maxPlayer
    
    else:
        #print('Made it here 2')
        (_, xPos, yPos) = maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
        if xPos is not None and yPos is not None:
            #print('Made it here X')
            move = [xPos, yPos]
            return move
        else:
            move = getMove(board, maxPlayer, boardSize, winThreshold)
            return move


      
def alphaBetaSearch(boardSize, winThreshold):
    
    board = createBoard(boardSize)
    
    maxPlayer = 'X'
    minPlayer = 'O'
    alpha = -float("inf")
    beta = float("inf")
    #Currently not working
    currentDepth = 0
    maxDepth = 4 
    
    player = maxPlayer
    turnCounter = 0
    while True:
        
        drawBoard(board)
        #print(turnCounter)
        result = checkForWin(board, boardSize, winThreshold)
        if result != None:
            if result == 'X':
                print('X wins')
            elif result == 'O':
                print('O wins')
            elif result == '-':
                print('Tie')
            return
            
        if player == maxPlayer:
            if turnCounter == 0:
                
               bestFirstMoves = pickFirstMove(board, boardSize, minPlayer)
               if bestFirstMoves:
                   r.shuffle(bestFirstMoves)
                   firstMove = bestFirstMoves[0]
                   board[firstMove[0]][firstMove[1]] = maxPlayer
                   
            else:    
                (_, xPos, yPos) = maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
                if xPos is not None and yPos is not None:
                    #print('Made it here X')
                    board[xPos][yPos] = maxPlayer
                else:
                    move = getMove(board, maxPlayer, boardSize, winThreshold)
                    #print(move)
                    board[move[0]][move[1]] = maxPlayer
            player = minPlayer
            turnCounter = turnCounter + 1
            
        else:
            if turnCounter == 1:
                
               bestFirstMoves = pickFirstMove(board, boardSize, maxPlayer)
               if bestFirstMoves:
                   r.shuffle(bestFirstMoves)
                   firstMove = bestFirstMoves[0]
                   board[firstMove[0]][firstMove[1]] = minPlayer
            else:
                (_, xPos, yPos) = minValue(board, maxPlayer, minPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
                
                if xPos is not None and yPos is not None:
                    #print('Made it here O')
                    board[xPos][yPos] = minPlayer
                else:
                    move = getMove(board, minPlayer, boardSize, winThreshold)
                    board[move[0]][move[1]] = minPlayer
            player = maxPlayer
            turnCounter = turnCounter + 1
               
if __name__ == "__main__":

    #alphaBetaSearch(8, 5)
    alphaBetaSearch(9, 5)