import time


def encode(elem1, elem2):
    return str(elem1) + "-" + str(elem2)


def decode(elem1):
    split = elem1.split('-')
    return int(split[0]), int(split[1])


def buildImp(i, j, board):  # Build Implications Table impTableItem = key : val not entire dictionary
    impTableItem = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Check Row
    for val in board[i]:
        if val != 0:
            if impTableItem.count(val) > 0:
                impTableItem.remove(val)

    # Check Col
    for y in range(len(board)):
        if board[y][j]:
            if impTableItem.count(board[y][j]) > 0:
                impTableItem.remove(board[y][j])

    yStart, xStart = 3 * (i // 3), 3 * (j // 3)
    for y in range(yStart, yStart + 3):
        for x in range(xStart, xStart + 3):
            if board[y][x]:
                if impTableItem.count(board[y][x]) > 0:
                    impTableItem.remove(board[y][x])

    return impTableItem


def updateImpTable(board):
    impTable = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                name = encode(i, j)
                impTable[name] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                impTable[name] = buildImp(i, j, board)
    return impTable


def search(board, impTable, backTrack):
    solutionFound = False
    guesses = []  # Store which impTable keys have been used as guess
    while not solutionFound:
        while not backTrack:

            delKey, update = [], False
            minLen, minKey = 10, None

            for key in impTable:

                keyLength = len(impTable[key])
                if keyLength == 0:
                    # print("Illegal Key length found, backtracking")
                    backTrack = True
                    break

                if keyLength == 1:
                    update = True
                    i, j = decode(key)
                    board[i][j] = impTable[key][0]
                    delKey.append(key)
                    # print(f"Updating board{i, j} with singleton {impTable[key][0]}")
                    # for row in board:
                    #     print(row)
                    if len(guesses) > 0:
                        guesses.append([key, []])
                        # print("Appending singleton to guess list")
                        # print(guesses)
                    break
                elif keyLength < minLen:
                    minLen, minKey = keyLength, key
            for item in delKey:
                del impTable[item]

            if update:  # A singleton was found.
                impTable = updateImpTable(board)
                # print("If Update: impTable")
                # for key in impTable:
                #     print(f"{key} : {impTable[key]}")
            elif not backTrack:  # A singleton was not found. Make a guess

                y, x = decode(minKey)
                board[y][x] = impTable[minKey][-1]  # Set board to guess
                # print(f'Setting board with guess: {minKey} : {impTable[minKey]}')
                # for row in board:
                #     print(row)
                impTable[minKey].pop()  # Remove guess from impTable
                guesses.append([minKey, impTable[minKey].copy()])  # Keep track of keys remaining guesses
                # print(f"Guess List updated: {guesses}")
                impTable = updateImpTable(board)
                # print(f"Guess made impTable: ")
                # for key in impTable:
                #     print(f"{key} : {impTable[key]}")

            if len(impTable) == 0:
                print("Solution Found")
                backTrack = True
                solutionFound = True
                for row in board:
                    print(row)
                # for key in impTable:
                #     print(f"{key} : {impTable[key]}")

        while backTrack and not solutionFound:
            # print(f"Guesses (backTracking): {guesses}")
            y, x = decode(guesses[-1][0])  # Get last index that was updated with a guess
            if len(guesses[-1][1]) == 0:
                board[y][x] = 0
                guesses.pop()
            else:
                board[y][x] = guesses[-1][1][-1]  # Put a new guess in
                guesses[-1][1].pop()  # Remove the guess
                backTrack = False
                impTable = updateImpTable(board)
                # print("Last impTable")
                # print(len(impTable))
                # for key in impTable:
                #     print(f"{key} : {impTable[key]}")
                # for row in board:
                #     print(row)
                # print(f"Solution Found: {solutionFound}")
    return board


def solve(board):
    impTable = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                name = encode(i, j)
                impTable[name] = None
                impTable[name] = buildImp(i, j, board)

    # print("Implications Table")
    # for key in impTable:
    #     print(f"{key} : {impTable[key]}")
    return search(board, impTable, False)


problem = [[0, 0, 7, 0, 0, 5, 0, 0, 3],
           [0, 3, 0, 0, 9, 0, 0, 4, 0],
           [9, 0, 0, 1, 0, 0, 8, 0, 0],
           [4, 0, 0, 6, 0, 0, 5, 0, 0],
           [0, 7, 0, 0, 3, 0, 0, 1, 0],
           [0, 0, 5, 0, 0, 9, 0, 0, 6],
           [0, 0, 4, 0, 0, 7, 0, 0, 2],
           [0, 8, 0, 0, 2, 0, 0, 5, 0],
           [2, 0, 0, 8, 0, 0, 4, 0, 0]]

# problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
#            [0, 0, 0, 4, 0, 6, 0, 0, 0],
#            [0, 0, 5, 0, 7, 0, 3, 0, 0],
#            [0, 6, 0, 0, 0, 0, 0, 4, 0],
#            [4, 0, 1, 0, 6, 0, 5, 0, 8],
#            [0, 9, 0, 0, 0, 0, 0, 2, 0],
#            [0, 0, 7, 0, 3, 0, 2, 0, 0],
#            [0, 0, 0, 7, 0, 5, 0, 0, 0],
#            [1, 0, 0, 0, 4, 0, 0, 0, 7]]

#
# problem = [[9, 2, 0, 0, 8, 0, 0, 0, 1],
#            [0, 0, 3, 4, 0, 6, 0, 0, 0],
#            [0, 0, 5, 9, 7, 0, 3, 0, 0],
#            [0, 6, 0, 0, 5, 0, 0, 4, 0],
#            [4, 0, 1, 0, 6, 0, 5, 0, 8],
#            [0, 9, 0, 0, 0, 0, 0, 2, 0],
#            [0, 0, 7, 0, 3, 0, 2, 0, 0],
#            [0, 0, 0, 7, 0, 5, 0, 0, 0],
#            [1, 0, 0, 0, 4, 0, 0, 0, 7]]

extreme = [[2, 0, 0, 0, 0, 0, 0, 5, 0],
           [0, 0, 8, 0, 3, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 4, 0, 0, 2, 6, 0],
           [0, 1, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 0, 0, 0, 0, 0],
           [6, 0, 0, 0, 0, 0, 1, 0, 3],
           [4, 0, 0, 5, 0, 9, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 7, 0, 0]]

easy = [[9, 0, 6, 5, 8, 3, 4, 7, 1],
        [7, 1, 3, 4, 2, 6, 9, 8, 5],
        [8, 4, 5, 9, 7, 1, 3, 6, 2],
        [3, 6, 2, 8, 5, 7, 1, 4, 9],
        [4, 7, 1, 2, 6, 9, 5, 3, 8],
        [5, 9, 8, 3, 1, 4, 7, 2, 6],
        [6, 5, 7, 1, 3, 8, 2, 9, 4],
        [2, 8, 4, 0, 9, 5, 6, 1, 3],
        [1, 3, 9, 6, 4, 0, 8, 0, 7]]

tic = time.perf_counter()
result = solve(extreme)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
for row in result:
    print(row)
#
# solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1],
#             [7, 1, 3, 4, 2, 6, 9, 8, 5],
#             [8, 4, 5, 9, 7, 1, 3, 6, 2],
#             [3, 6, 2, 8, 5, 7, 1, 4, 9],
#             [4, 7, 1, 2, 6, 9, 5, 3, 8],
#             [5, 9, 8, 3, 1, 4, 7, 2, 6],
#             [6, 5, 7, 1, 3, 8, 2, 9, 4],
#             [2, 8, 4, 7, 9, 5, 6, 1, 3],
#             [1, 3, 9, 6, 4, 2, 8, 5, 7]]
