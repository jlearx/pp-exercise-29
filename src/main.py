'''
Created on Sep 27, 2017

@author: jlearx
'''

NOWINNER = "No winner yet. Game not over."
PLAYER1WON = "Game over! Player 1 Won!"
PLAYER2WON = "Game over! Player 2 Won!"
DRAW = "Game over! Draw!"

# Number of columns
COLSIZE = 3

# Number of rows
ROWSIZE = 3

# Number needed to WIN
TOWIN = 3

def checkInARow(row):
    # Can't win if there is a 0 in the row
    if (0 in row):
        return NOWINNER
    elif (row.count(1) == TOWIN):
        # Does not guarantee a win if length > TOWIN
        return PLAYER1WON
    elif (row.count(2) == TOWIN):
        # Does not guarantee a win if length > TOWIN
        return PLAYER2WON
    else:
        return DRAW    

def checkHorizontal(gameBoard):
    finalResult = DRAW
    result = DRAW
    rowIdx = 0
    
    while (((result == NOWINNER) or (result == DRAW)) and (rowIdx < ROWSIZE)):
        row = gameBoard[rowIdx]
        result = checkInARow(row)
        
        if (result == NOWINNER):
            finalResult = NOWINNER
        elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
            return result
        
        rowIdx += 1

    return finalResult

def checkVertical(gameBoard):
    finalResult = DRAW
    result = DRAW
    colIdx = 0
    
    while (((result == NOWINNER) or (result == DRAW)) and (colIdx < COLSIZE)):
        row = []
        
        for rowIdx in range(0,ROWSIZE):
            row.append(gameBoard[rowIdx][colIdx])
        
        result = checkInARow(row)
        
        if (result == NOWINNER):
            finalResult = NOWINNER
        elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
            return result
        
        colIdx += 1

    return finalResult

def checkDiagonal(gameBoard):
    # Broken for grids bigger than size 3
    finalResult = DRAW
    
    # Check first diagonal
    row = [gameBoard[0][0], gameBoard[1][1], gameBoard[2][2]]
    result = checkInARow(row)
    
    if (result == NOWINNER):
        finalResult = NOWINNER
    elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
        return result    
    
    # Check second diagonal    
    row = [gameBoard[0][2], gameBoard[1][1], gameBoard[2][0]]
    result = checkInARow(row)        
        
    if (result == NOWINNER):
        finalResult = NOWINNER
    elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
        return result

    return finalResult    

def checkWinner(gameBoard):
    finalResult = DRAW
    
    # Check for horizontal wins
    result = checkHorizontal(gameBoard)
    
    if (result == NOWINNER):
        finalResult = NOWINNER
    elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
        return result    
    
    # Check for vertical wins
    result = checkVertical(gameBoard)
    
    if (result == NOWINNER):
        finalResult = NOWINNER
    elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
        return result
    
    # Check for diagonal wins
    result = checkDiagonal(gameBoard)
    
    if (result == NOWINNER):
        finalResult = NOWINNER
    elif ((result == PLAYER1WON) or (result == PLAYER2WON)):
        return result
        
    return finalResult

def getGameBoardSize():
    global ROWSIZE, COLSIZE, TOWIN
    ROWSIZE = 0
    COLSIZE = 0
    
    while ((ROWSIZE < 1) and (COLSIZE < 1)): 
        inputStr = ""
        xPos = -1
        
        while (inputStr == ""):
            inputStr = input("Please enter the game board dimensions as wxh (eg. 3x3): ").strip()
            inputStr = inputStr.lower()
            
            if (len(inputStr) < 3):
                inputStr = ""                
                continue
            
            xPos = inputStr.find('x')
            
            if ((xPos < 1) or (xPos == len(inputStr) - 1)):
                inputStr = ""                
                continue
        
        # Width (number of columns)
        COLSIZE = int(inputStr[:xPos])
        
        # Height (number of rows)
        ROWSIZE = int(inputStr[xPos + 1:])
    
    # How many in a row should the user need to win?
    if (ROWSIZE <= COLSIZE):
        TOWIN = ROWSIZE
    else:
        TOWIN = COLSIZE

def printRowBorder():
    for i in range(0,COLSIZE):
        print(" ---", end="")
        
    print(" ")
    
def printColumn(gameBoard, row):
    for col in range(0,COLSIZE):
        state = gameBoard[row][col]
        
        print("| ", end="")
        
        if (state == 1):
            print("X", end="")
        elif (state == 2):
            print("O", end="")
        else:
            print(" ", end="")
            
        print(" ", end="")
    
    print("|")

def printGameBoard(gameBoard):
    for row in range(0,ROWSIZE):
        printRowBorder()
        printColumn(gameBoard, row)
    
    printRowBorder()

def getMove(gameBoard):
    # Display game state
    printGameBoard(gameBoard)
    
    # Repeat until a valid move is given
    while (True):
        moveStr = input("Please enter a valid move as row,col (y,x): ").strip()
        row = -1
        col = -1        
        
        # Check input length
        if (len(moveStr) < 3):
            continue
        
        # Check if input contains a comma
        cPos = moveStr.find(',')
        
        if ((cPos < 1) or (cPos == len(moveStr) - 1)):
            continue
        
        # Parse move out of input string
        row = moveStr[:cPos]
        col = moveStr[cPos + 1:]
        
        # Make sure the row and column are numeric
        if (row.isnumeric() and col.isnumeric()):
            # Reduce by 1 because we start from 0
            row = int(row) - 1
            col = int(col) - 1
        else:
            continue
        
        # Make sure the row and column are within bounds
        if ((row < 0) or (col < 0) or (row >= ROWSIZE) or (col >= COLSIZE)):
            continue
        
        # Check if move is in a free square (0)
        if (gameBoard[row][col] == 0):
            return (row,col)
        else:
            # Show the board again
            printGameBoard(gameBoard)

def makeMove(gameBoard, move, p1Turn):
    # Parse out the move
    row = move[0]
    col = move[1]
    
    # Update the Game Board
    if (p1Turn):
        gameBoard[row][col] = 'X'
    else:
        gameBoard[row][col] = 'O'

def checkGameOver(gameBoard):
    gameOver = True
    
    for row in gameBoard:
        if (0 in row):
            gameOver = False
            
    return gameOver

def playGame(gameBoard):
    p1Turn = True
    gameOver = False
    
    # Take turns and switch player at end of turn
    while (True):
        if (p1Turn):
            print("Player 1's Turn")
        else:
            print("Player 2's Turn")
        
        # Get the player's move
        move = getMove(gameBoard)
        
        # Update the game board with move
        makeMove(gameBoard, move, p1Turn)
        
        # Check the game state
        gameOver = checkGameOver(gameBoard)
        
        if (gameOver):
            break
        
        # Switch current player
        if (p1Turn):
            p1Turn = False
        else:
            p1Turn = True

    print("GAME OVER")
    printGameBoard(gameBoard)

def newGame():
    gameBoard = []
    
    getGameBoardSize()

    # Initialize Game Board
    for r in range(0,ROWSIZE):
        row = []
        
        for c in range(0,COLSIZE):
            row.append(0)
            
        gameBoard.append(row)
            
    return gameBoard
    
if __name__ == '__main__':
    gameBoard = newGame()
    printGameBoard(gameBoard)

    #playGame(gameBoard)
        
    