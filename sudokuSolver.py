import time
xStartList = {
    "012": {
        '012': [0, 0],
        '345': [0, 3],
        '678': [0, 6]
    },
    '345': {
        '012': [3, 0],
        '345': [3, 3],
        '678': [3, 6]
    },
    '678': {
        '012': [6, 0],
        '345': [6, 3],
        '678': [6, 6]
    }
}


def checkSolution(checkVal, checkValPos, board):
    # print(f"Checking {checkVal} at [{checkValPos[0]}, {checkValPos[1]}] : {board[checkValPos[0]]}")
    # Check Row
    if checkVal in board[checkValPos[0]]:
        # print("Failed row check")
        return False

    # Check Col
    temp = []
    for y in range(len(board)):
        if board[y][checkValPos[1]] != 0:
            temp.append(board[y][checkValPos[1]])
    if checkVal in temp:
        # print('Failed Col Check')
        return False

    xPatternStart = None
    for key in xStartList:
        if xPatternStart:
            break
        if str(checkValPos[0]) in key:
            for subKey in xStartList[key]:
                if str(checkValPos[1]) in subKey:
                    xPatternStart = xStartList[key][subKey]
                    break
    temp = []
    for y in range(xPatternStart[0], xPatternStart[0] + 3):
        for x in range(xPatternStart[1], xPatternStart[1] + 3):
            if board[y][x] != 0:
                temp.append(board[y][x])
    if checkVal in temp:
        # print("Failed X Check")
        return False
    return True


def findNextYX(y, x, backTrack):
    if y == 8 and x == 8:
        return "Result Found", None
    # print(f"Searching for next mutable index at [{y, x}]")
    if not backTrack:
        if x == 8:
            x = 0
            y += 1
        else:
            x += 1
        return y, x
    else:
        if x == 0:
            x = 8
            y -= 1
        else:
            x -= 1
        return y, x


def recursiveSearch(y, x, board, immutableValues, backTrack):
    solutionFound = False
    while not solutionFound:
        while not backTrack:
            # print(f"Check if {x} is in {immutableValues[y]}")
            if x in immutableValues[y]:
                y, x = findNextYX(y, x, backTrack)
                if y == "Result Found":
                    backTrack, solutionFound = False, True
                    break
            else:
                if board[y][x] < 9:
                    checkVal = board[y][x] + 1
                    if checkSolution(checkVal, [y, x], board):
                        board[y][x] = checkVal
                        y, x = findNextYX(y, x, backTrack)
                        if y == "Result Found":
                            backTrack, solutionFound = False, True
                            break
                    else:
                        board[y][x] = checkVal
                else:
                    board[y][x] = 0
                    backTrack = True
                    y, x = findNextYX(y, x, backTrack)
                    if y == "Result Found":
                        backTrack, solutionFound = False, True
                        break
        while backTrack:
            if y == "Result Found":
                backTrack, solutionFound = False, True
                break
            if x in immutableValues[y]:
                y, x = findNextYX(y, x, backTrack)
            elif board[y][x] == 9:
                board[y][x] = 0
                y, x = findNextYX(y, x, backTrack)
            else:
                backTrack = False
    print("Finished")
    for row in board:
        print(row)


def solve(board):
    immutableValues = {}
    # Build immutable table
    for i in range(len(board)):
        immutableValues[i] = []
        for j in range(len(board[i])):
            if board[i][j] != 0:
                immutableValues[i].append(j)

    recursiveSearch(0, 0, board, immutableValues, False)


# 9 , 0, 0 : 0, 1 = {2,3,4,7}, 0, 2 = {2, 3, 4, 6, 8}, 1, 0 = {1, 2, 3, 7, 8}, 1, 1 = {1,2,3,7,8} 1, 2 = {1, 2, 3, 8}
# 0, 0, 0
# 0, 0, 5

# Create implications table
# If imp length = 1, add value to board and immutables, delete from table?
# Continue
# If no imp table len = 1, find shortest and guess


problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
           [0, 0, 0, 4, 0, 6, 0, 0, 0],
           [0, 0, 5, 0, 7, 0, 3, 0, 0],
           [0, 6, 0, 0, 0, 0, 0, 4, 0],
           [4, 0, 1, 0, 6, 0, 5, 0, 8],
           [0, 9, 0, 0, 0, 0, 0, 2, 0],
           [0, 0, 7, 0, 3, 0, 2, 0, 0],
           [0, 0, 0, 7, 0, 5, 0, 0, 0],
           [1, 0, 0, 0, 4, 0, 0, 0, 7]]

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
solve(problem)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
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

#
# if x not in immutableValues[y]:  # Check for mutable Values
#     newVal = board[y][x] + 1
#     if newVal > 9:
#         board[y][x] = 0
#         if x == 0:
#             y -= 1
#             x = 9
#         print("+___________________________")
#         recursiveSearch(y, x - 1, board, False)
#     elif checkSolution(newVal, [y, x], board):
#         board[y][x] = newVal
#         if x == 8:
#             y += 1
#             x = -1
#         print("^___________________________")
#         recursiveSearch(y, x + 1, board, True)
#     else:
#         print("&___________________________")
#         board[y][x] = newVal
#         recursiveSearch(y, x, board, True)
# else:
#     if lookForward:
#         if x == 8:
#             y += 1
#             x = -1
#         print("!___________________________")
#         recursiveSearch(y, x + 1, board, True)
#     elif not lookForward:
#         if x == 0:
#             x = 9
#             y -= 1
#         recursiveSearch(y, x - 1, board, False)
