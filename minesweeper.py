
import time
import sys
search = [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]]
solution = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()
solutionMap = [x.split() for x in solution.split('\n')]  # For Testing


def inBounds(position, gameMap):
    if 0 <= position[0] < len(gameMap) and 0 <= position[1] < len(gameMap[0]):
        return True


def _open(gvp):  # Grid Value Position
    return solutionMap[gvp[0]][gvp[1]]


def printGM(gameMap):
    print("")
    for row in gameMap:
        print(row)


def markGiven(gameMap):  # Zero found
    def openAll(gvp, _gameMap):
        for directions in search:
            searchPos = [gvp[0] + directions[0], gvp[1] + directions[1]]
            if inBounds(searchPos, gameMap):
                if gameMap[searchPos[0]][searchPos[1]] == "?":
                    gridVal = _open([searchPos[0], searchPos[1]])
                    _gameMap[searchPos[0]][searchPos[1]] = gridVal
        return _gameMap

    for rowIdx, row in enumerate(gameMap):
        for colIdx, col in enumerate(row):
            if col == '0':
                gameMap = openAll([rowIdx, colIdx], gameMap)
    return gameMap


def markFound(gameMap, positions, id):
    for pos in positions:
        if id == "safe":
            gridVal = _open(pos)
            gameMap[pos[0]][pos[1]] = gridVal
        elif id == "mine":
            gameMap[pos[0]][pos[1]] = "x"
    return gameMap


def searchSurrounding(gvp, gameMap):
    minesFound, unknowns = 0, 0
    minePositions, unknownPositions = [], []
    for directions in search:
        searchPos = [gvp[0] + directions[0], gvp[1] + directions[1]]
        if inBounds(searchPos, gameMap):
            if gameMap[searchPos[0]][searchPos[1]] == "x":
                minesFound += 1
            elif gameMap[searchPos[0]][searchPos[1]] == "?":
                unknowns += 1
                unknownPositions.append([searchPos[0], searchPos[1]])
    return minesFound, unknowns, unknownPositions


def patternCheck(gameMap, pattern, pT, searchPos):  # patternType
    if pT == '1':
        if pattern == "23":
            print(f'Type 1 regular pattern found near {searchPos} (Above)')
            searchPos[0] -= 1  # Position to open
            searchPos[1] += 1  # Position to open
            if inBounds(searchPos, gameMap):
                gameMap = markFound(gameMap, [searchPos], "safe")
        elif pattern == '32':
            print(f'Type 1 reverse pattern found near {searchPos} (Above)')
            searchPos[0] -= 1  # Position to open
            searchPos[1] -= 2  # Position to open
            if inBounds(searchPos, gameMap):
                gameMap = markFound(gameMap, [searchPos], "safe")
    return gameMap


def findMines(gameMap):
    gameOver = False
    rowSolved = []
    count = 0
    # while not gameOver:
    pattern1_1 = ''
    pattern1_2 = ''
    while count < 7:

        for rowIdx, row in enumerate(gameMap):
            print(f"Checking row {rowIdx}")
            if rowIdx in rowSolved:
                pass
            rowSolutions = 0
            for colIdx, col in enumerate(row):
                if col.isnumeric():
                    rowSolutions += 1
                if col.isnumeric() and int(col) > 0:
                    # print(f'Checking {col} at position {rowIdx, colIdx}')
                    position = [rowIdx, colIdx]
                    minesFound, unknowns, unknownPositions = searchSurrounding(position, gameMap)
                    if minesFound == int(col) and unknowns > 0:
                        gameMap = markFound(gameMap, unknownPositions, "safe")
                        # printGM(gameMap)
                    elif unknowns + minesFound == int(col):
                        gameMap = markFound(gameMap, unknownPositions, "mine")
                        # printGM(gameMap)
                    #  Pattern Testing
                    patternInit = True
                    if int(col) - minesFound == 1:
                        if unknowns == 2:
                            pattern1_1 += '2'
                        elif unknowns == 3:
                            pattern1_1 += '3'
                        else:
                            patternInit = False
                        if patternInit:
                            gameMap = patternCheck(gameMap, pattern1_1, "1", position)
                        else:
                            pattern1_1 = ''
                        if len(pattern1_1) == 2:
                            pattern1_1 = ''
                if rowSolutions == len(gameMap[0]):
                    rowSolved.append(rowIdx)
        count += 1


def solve_mine(_map, n):
    gameMap = [x.split() for x in _map.split('\n')]
    gameMap = markGiven(gameMap)
    findMines(gameMap)


gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()




tic = time.perf_counter()
solve_mine(gamemap, 2)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")


# If you find a value, if there are the same number of mines touching the square, open all.
# If there are the same number of ? touching position. Mark question mark as a mine

# Average .07ish