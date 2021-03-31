#!/usr/bin/env yPosthon3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 19:39:27 2021

@author: kingrice
"""

from itertools import groupby
import numpy as np
    
def createBoard(n):
    board = [['.' for col in range(n)] for row in range(n)]
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
        if len(longestRun[1]) == winThreshold and longestRun[0] != '.':
            return longestRun[0]
            
    #Horizontal win
    for row in range(0, boardSize):
        listOfRuns = [(symbol, list(run)) for symbol, run in groupby(board[row])]
        longestRun = max(listOfRuns, key=lambda x:len(x[-1]))
        if len(longestRun[1]) == winThreshold and longestRun[0] != '.':
            return longestRun[0]
        
        
    #Diagonal win
    npBoard = np.array(board)
    diags = [npBoard[::-1,:].diagonal(i) for i in range(-npBoard.shape[0]+1,npBoard.shape[1])]
    diags.extend(npBoard.diagonal(i) for i in range(npBoard.shape[1]-1,-npBoard.shape[0],-1))
    for d in diags:
        if len(d) >= winThreshold:
            listOfRuns = [(symbol, list(run)) for symbol, run in groupby(d.tolist())]
            longestRun = max(listOfRuns, key=lambda x:len(x[-1]))
            if len(longestRun[1]) == winThreshold and longestRun[0] != '.':
                return longestRun[0]
    
    #Check if board is full
    for row in range(0, boardSize):
        for col in range(0, boardSize):
            if board[row][col] == '.':
                return None
    
    return '.'

def terminalTest(board, minPlayer, maxPlayer, boardSize, winThreshold):
    
    # Return Utility(state)
    winner = checkForWin(board, boardSize, winThreshold)
    if winner == minPlayer:
        return (-1, 0, 0)
    elif winner == maxPlayer:
        return (1, 0, 0)
    elif winner == '.':
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
    
    #if currentDepth < maxDepth:
    for row in range (0,boardSize):
        for col in range (0,boardSize):
            if board[row][col] == '.':
                board[row][col] = maxPlayer
                (mValue, _, _) = minValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
        
                if mValue > value:
                    value = mValue
                    xPos = row
                    yPos = col
                board[row][col] = '.'
                
                if value >= beta:
                    return (value, xPos, yPos)
                
                alpha = max(alpha, value)
    
    #else:
    #    (xPos, yPos) = getEmptyAdjacentSqaures(refX, refY, board)
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
    
    #if currentDepth < maxDepth:
    for row in range (0,boardSize):
        for col in range (0,boardSize):
            if board[row][col] == '.':
                board[row][col] = minPlayer
                (mValue, _, _) = maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth + 1, maxDepth, boardSize, winThreshold)
                #print(m)
                if mValue < value:
                    value = mValue
                    xPos = row
                    yPos = col 
                board[row][col] = '.'
                
                if value <= alpha:
                    return (value, xPos, yPos)
                
                beta = min(beta, value)
    
    #else:
    #    (xPos, yPos) = getEmptyAdjacentSqaures(refX, refY, board)
    return (value, xPos, yPos)
       
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
    
    while True:
        
        drawBoard(board)
        result = checkForWin(board, boardSize, winThreshold)
        
        if result != None:
            if result == 'X':
                print('X wins')
            elif result == 'O':
                print('O wins')
            elif result == '.':
                print('Tie')
            return
            
        if player == maxPlayer:
            (_, xPos, yPos) = maxValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
            board[xPos][yPos] = maxPlayer
            player = minPlayer
            
        else:
            (_, xPos, yPos) = minValue(board, minPlayer, maxPlayer, alpha, beta, currentDepth, maxDepth, boardSize, winThreshold)
            board[xPos][yPos] = minPlayer
            player = maxPlayer
                
if __name__ == "__main__":

    alphaBetaSearch(3, 3)