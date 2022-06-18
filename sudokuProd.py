import time
import sys


def encode(elem1, elem2):
    return str(elem1) + "-" + str(elem2)


def decode(elem1):
    split = elem1.split('-')
    return int(split[0]), int(split[1])


# i : y, j : x
def buildImp(i, j, board, initCheck):  # Build Implications Table impTableItem = key : val not entire dictionary
    impTableItem = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Check Row
    for val in board[i]:
        if val:
            if impTableItem.count(val) == 1:
                impTableItem[val - 1] = "x"
            else:
                print("Illegal Board")
                return False
    # Check Col/ Build Vertical Check List
    vertCheck = []
    for y in range(len(board)):
        if board[y][j]:
            impTableItem[board[y][j] - 1] = "x"
            vertCheck.append(board[y][j])
    if initCheck:
        for val in vertCheck:
            if vertCheck.count(val) > 1:
                print("Illegal Board")
                return False

    yStart, xStart = 3 * (i // 3), 3 * (j // 3)
    xCheck = []
    for y in range(yStart, yStart + 3):
        for x in range(xStart, xStart + 3):
            if board[y][x]:
                impTableItem[board[y][x] - 1] = "x"
                xCheck.append((board[y][x]))
    if initCheck:
        for val in xCheck:
            if xCheck.count(val) > 1:
                print("Illegal Board")
                return False

    temp = []
    for val in impTableItem:
        if val != "x":
            temp.append(val)

    return temp


def updateImpTable(board):
    impTable = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                name = encode(i, j)
                impTable[name] = None
                impTable[name] = buildImp(i, j, board, False)
    return impTable


def search(board, impTable, backTrack):
    solutionFound = False
    guesses = []  # Store which impTable keys have been used as guess
    while not solutionFound:
        while not backTrack:

            update = False
            minLen, minKey = 10, None

            for key in impTable:

                keyLength = len(impTable[key])
                if keyLength == 0:
                    backTrack = True
                    break

                if keyLength == 1:
                    update = True
                    i, j = decode(key)
                    board[i][j] = impTable[key][0]
                    if len(guesses) > 0:
                        guesses.append([key, []])
                        break
                elif keyLength < minLen:
                    minLen, minKey = keyLength, key

            if update:  # A singleton was found.
                impTable = updateImpTable(board)
            elif not backTrack:  # A singleton was not found. Make a guess

                y, x = decode(minKey)
                board[y][x] = impTable[minKey][-1]  # Set board to guess
                impTable[minKey].pop()  # Remove guess from impTable
                guesses.append([minKey, impTable[minKey].copy()])  # Keep track of keys remaining guesses
                impTable = updateImpTable(board)
            if len(impTable) == 0:
                backTrack = True
                solutionFound = True

        while backTrack and not solutionFound:
            y, x = decode(guesses[-1][0])  # Get last index that was updated with a guess
            if len(guesses[-1][1]) == 0:
                board[y][x] = 0
                guesses.pop()
            else:
                board[y][x] = guesses[-1][1][-1]  # Put a new guess in
                guesses[-1][1].pop()  # Remove the guess
                if len(guesses) == 1:
                    guesses = []
                backTrack = False
                impTable = updateImpTable(board)

    return board


def sudoku_solver(board):
    print("Start", flush=True)
    impTable = {}
    totalGiven = 0
    uniqueValues = []
    for idx in range(len(board)):
        if len(board[idx]) != 9:
            raise Exception("Illegal Board")
    if len(board) != 9:
        raise Exception("Illegal Board")
    for row in board:
        for element in row:
            if 0 > element > 9:
                raise Exception("Illegal Board")

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                name = encode(i, j)
                impTable[name] = None
                impTable[name] = buildImp(i, j, board, True)
                if not impTable[name]:
                    raise Exception("Illegal Board")
            else:
                totalGiven += 1
                if uniqueValues.count(board[i][j]) == 0:
                    uniqueValues.append(board[i][j])
    print(totalGiven)
    if totalGiven < 17:
        raise Exception("Illegal Board")
    if len(uniqueValues) < 8:
        raise Exception("Illegal Board")
    return search(board, impTable, False)


extreme = [[2, 0, 0, 0, 0, 0, 0, 5, 0],
           [0, 0, 8, 0, 3, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 4, 0, 0, 2, 6, 0],
           [0, 1, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 0, 0, 0, 0, 0],
           [6, 0, 0, 0, 0, 0, 1, 0, 3],
           [4, 0, 0, 5, 0, 9, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 7, 0, 0]]

problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],

           [0, 0, 0, 4, 0, 6, 0, 0, 0],
           [0, 0, 5, 0, 7, 0, 3, 0, 0],
           [0, 6, 0, 0, 0, 0, 0, 4, 0],
           [4, 0, 1, 0, 6, 0, 5, 0, 8],
           [0, 9, 0, 0, 0, 0, 0, 2, 0],
           [0, 0, 7, 0, 3, 0, 2, 0, 0],
           [0, 0, 0, 7, 0, 5, 0, 0, 0],
           [1, 0, 0, 0, 4, 0, 0, 0, 7]]

problem2 = [[4, 0, 5, 0, 1, 0, 7, 0, 8],
            [0, 0, 7, 0, 0, 5, 0, 0, 0],
            [0, 3, 0, 7, 0, 0, 0, 5, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 5],
            [0, 4, 0, 2, 0, 8, 0, 6, 0],
            [5, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 7, 0, 0, 2, 3, 0, 1, 0],
            [0, 0, 0, 4, 0, 0, 2, 0, 0],
            [9, 0, 6, 0, 7, 0, 4, 0, 3]]

tic = time.perf_counter()
result = sudoku_solver(problem2)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
print(result)
