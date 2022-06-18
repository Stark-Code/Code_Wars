import sys
import copy
import time


class ReversiBoard(object):

    @classmethod
    def translate(cls, coordinates):  # "d3"
        lower = [coordinates[0].lower(), coordinates[1]]
        translateRow = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        translateCol = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return translateRow[lower[1]], translateCol[lower[0]]

    @staticmethod
    def errorCheck(moveStr):
        legalChar = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        legalNum = ['1', '2', '3', '4', '5', '6', '7', '8']
        s = moveStr
        pairs = []
        while s:
            pairs.append(s[:2].lower())
            s = s[2:]
        errorsFound = 0
        for pair in pairs:
            if errorsFound > 0:
                break
            if pair[0] not in legalChar:
                errorsFound += 1
            if pair[1] not in legalNum:
                errorsFound += 1
        return errorsFound

    @staticmethod
    def buildBoard():
        return [["." for _ in range(8)] for _ in range(8)]

    @staticmethod
    def getPlayerTurn(turn):
        return turn ^ 1

    @staticmethod
    def initGame():
        board = ReversiBoard.buildBoard()
        playerTurn = 1
        board[4][3], board[3][4] = '1', '1'
        board[4][4], board[3][3] = '0', '0'
        return board, playerTurn

    @staticmethod
    def searchValidMove(pos, board, playerTurn, purpose):
        enemyToken = str(ReversiBoard.getPlayerTurn(playerTurn))
        attackedTokens = []
        if purpose == "attack":
            board[pos[0]][pos[1]] = str(playerTurn)
        validMove = False
        # print(f'PlayerToken: {playerTurn}, EnemyToken: {enemyToken}')
        searchParams = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]
        for directions in searchParams:
            if validMove and purpose == "check":
                break
            searchSquare = [pos[0] + directions[0], pos[1] + directions[1]]
            if purpose == "attack":
                pass
                # print(f'Examining board at {searchSquare} for attack')
            if 0 <= searchSquare[0] < 8 and 0 <= searchSquare[1] < 8:

                if board[searchSquare[0]][searchSquare[1]] == enemyToken:
                    # print(f'Enemy token {enemyToken} found at {searchSquare}')
                    attackedTokens.append(searchSquare)
                    while True:
                        searchSquare = [searchSquare[0] + directions[0], searchSquare[1] + directions[1]]
                        # print(f"Checking square: {searchSquare}")
                        if 0 <= searchSquare[0] < 8 and 0 <= searchSquare[1] < 8:
                            if board[searchSquare[0]][searchSquare[1]] == str(playerTurn):
                                if purpose == "attack":
                                    validMove = True
                                    # print(f"Swapping Tokens! {attackedTokens}")
                                    for token in attackedTokens:
                                        board[token[0]][token[1]] = str(playerTurn)
                                    break
                                else:
                                    print("No legal move found this direction")
                                    break
                            elif board[searchSquare[0]][searchSquare[1]] == ".":  # May need mod for attack
                                # print(f"Legal move found at {searchSquare}!")
                                attackedTokens = []
                                validMove = True
                                break
                            elif board[searchSquare[0]][searchSquare[1]] == enemyToken:
                                attackedTokens.append(searchSquare)
                        else:
                            attackedTokens = []
                            break
        return validMove

    @staticmethod
    def findPlayerToken(board, playerTurn):
        playerToken = str(playerTurn)
        for rowIdx in range(len(board)):
            for colIdx in range(len(board)):
                if board[rowIdx][colIdx] == playerToken:
                    # print(f'Player {playerTurn} token found at {(rowIdx, colIdx)}')
                    validMove = ReversiBoard.searchValidMove((rowIdx, colIdx), board, playerTurn, "check")
                    if validMove:
                        return True

    @staticmethod
    def callGameOver(board, gameState):  # Winner takes empty squares
        whiteScore, blackScore, empty = 0, 0, 0
        winner = None
        for row in board:
            for col in row:
                if col == "1":
                    whiteScore += 1
                elif col == "0":
                    blackScore += 1
                else:
                    empty += 1
        if whiteScore == blackScore:
            winner = "D"
        elif whiteScore > blackScore:
            if gameState != 'I':
                whiteScore += empty
            winner = "W"
        else:
            if gameState != 'I':
                blackScore += empty
            winner = "B"
        return whiteScore, blackScore, winner

    @classmethod
    def interpret_transcript(cls, move_str):
        board, playerTurn = ReversiBoard.initGame()
        errorCheck = ReversiBoard.errorCheck(move_str)
        if errorCheck:
            return "E", None, None, None, None
        for row in board:
            print(row)
        passMade = 0
        while True:
            playerTurn = ReversiBoard.getPlayerTurn(playerTurn)
            print(f'Next players turn!')
            legalMoves = ReversiBoard.findPlayerToken(board, playerTurn)  # Player has a potential move
            if legalMoves:
                if len(move_str) == 0:
                    gameState = "I"  # Incomplete - A player has a valid move
                    break
                move = move_str[:2]
                passMade = 0
                translateMove = cls.translate(move)
                print(f'Player {playerTurn} want to play move: {move} ({translateMove})')
                if board[translateMove[0]][translateMove[1]] != ".":  # Check to see if player is moving to an open spot
                    gameState = "E"
                    playerTurn = None
                    break
                legalAttack = ReversiBoard.searchValidMove((translateMove[0], translateMove[1]), board, playerTurn,
                                                           "attack")
                if not legalAttack:
                    gameState = "E"
                    playerTurn = None
                    break
                move_str = move_str[2:]  # Remove a play from string
                rowNum = 8
                for row in board:
                    print(rowNum, row)
                    rowNum -= 1
                print('    A,   B,   C,   D,   E,   F,   G,   H')
            else:  # No legal move was found for player
                passMade += 1
                if passMade >= 2:  # Call game over
                    gameState = "C"  # Complete - No players have a valid move
                    playerTurn = None
                    if len(move_str) != 0:
                        gameState = "E"
                        playerTurn = None
                    break
        #  Exit of game loop
        print("Exited game loop")
        whiteScore, blackScore, winner = ReversiBoard.callGameOver(board, gameState)
        print(f'gameState: {gameState}')
        if gameState == "E":
            winner = None
            whiteScore = None
            blackScore = None
            playerTurn = None
        elif gameState == "I":
            winner = "I"
        elif gameState == "C":
            playerTurn = None
        if winner == "D" and passMade > 1:
            whiteScore, blackScore = 32, 32
        print(f'whiteScore: {whiteScore}, blackScore: {blackScore}')
        print(f'Player Turn: {playerTurn}')
        if playerTurn == 1:
            playerTurn = "W"
        elif playerTurn == 0:
            playerTurn = "B"
        return gameState, playerTurn, winner, blackScore, whiteScore

tic = time.perf_counter()
# results = ReversiBoard.interpret_transcript('d3c3c4e3b2b3c2b4c5a1a2a3f5b1f2c1a4a5')
# results = ReversiBoard.interpret_transcript('a3')
results = ReversiBoard.interpret_transcript('f5f4f3g4e3e6g3d3c4c5c3b4d6d2g6f6e7e2f2h3b6g5f7c6h5d7h4e8h2a6c8g7g2h6d8h1h8h7e1g1f1d1c7b7a8b8c1c2b5a5g8f8b2b1a4a2a1b3a3a7')
print(f'State: {results[0]}, Turn: {results[1]}, Winner: {results[2]}, Black: {results[3]}, White: {results[4]}')
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

# Flipping too many tokens.

# Player 1 want to play move: g5 ((3, 6))
# 8 ['.', '.', '.', '.', '.', '.', '.', '.']
# 7 ['.', '.', '.', '.', '0', '.', '.', '.']
# 6 ['.', '0', '.', '0', '0', '1', '0', '.']
# 5 ['.', '.', '0', '0', '0', '0', '1', '.']
# 4 ['.', '1', '1', '0', '0', '1', '1', '.']
# 3 ['.', '.', '1', '1', '1', '1', '1', '1']
# 2 ['.', '.', '.', '1', '1', '0', '.', '.']
# 1 ['.', '.', '.', '.', '.', '.', '.', '.']
#     A,   B,   C,   D,   E,   F,   G,   H
# Next players turn!
# Player 0 want to play move: f7 ((1, 5))
# 8 ['.', '.', '.', '.', '.', '.', '.', '.']
# 7 ['.', '.', '.', '.', '0', '0', '.', '.']
# 6 ['.', '0', '.', '0', '0', '0', '0', '.']
# 5 ['.', '.', '0', '0', '0', '0', '1', '.']
# 4 ['.', '1', '1', '0', '0', '0', '1', '.']
# 3 ['.', '.', '1', '1', '1', '0', '1', '1']
# 2 ['.', '.', '.', '1', '1', '0', '.', '.']
# 1 ['.', '.', '.', '.', '.', '.', '.', '.']
#     A,   B,   C,   D,   E,   F,   G,   H
