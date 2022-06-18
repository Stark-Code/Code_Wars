import copy
import time
global answer


def validate(hint, solList):
    # print(f"Hint: {hint}")
    validSolutions = []
    for solution in solList:
        # print(f'Checking {solution}')

        hintStructure = []
        clueLen = 0
        for idx, item in enumerate(solution):
            if item == "1":
                clueLen += 1
            if item == "0" or idx == len(solution)-1:
                if clueLen > 0:
                    hintStructure.append(clueLen)
                    clueLen = 0
        # print(f'Hint Structure: {hintStructure}')
        if tuple(hintStructure) == hint:
            # print("Valid Solution Found")
            validSolutions.append(solution)
    return validSolutions


def incrementStrSolution(solution):
    solution += 1
    return solution, "{0:05b}".format(solution)


def searchSolutions(bS):
    solution, strSols, limit = 0, [], "1" * bS
    while True:
        solution, strSol = incrementStrSolution(solution)
        strSols.append(strSol)
        if strSol == limit:
            break
    return strSols


def limitSolutions(rowSolutions, colSolutions):
    for col in colSolutions:
        if len(colSolutions[col]) == 1:
            for idx in range(len(colSolutions[col][0])):
                removals = []
                # print(f'idx: {idx}, val: {colSolutions[col][0][idx]}, {colSolutions[col]}')
                for solIdx, sol in enumerate(rowSolutions[idx]):
                    if sol[col] != colSolutions[col][0][idx]:
                        removals.append(rowSolutions[idx][solIdx])
                for remove in removals:
                    rowSolutions[idx].pop(rowSolutions[idx].index(remove))

    return rowSolutions


def checkBoard(board, colSolutions):
    global answer
    column = ""
    for colIdx in range(len(board)):
        for rowIdx in range(len(board[colIdx])):
            column += board[rowIdx][colIdx]
        if column not in colSolutions[colIdx]:
            return False
        column = ""
    answer = board
    return True


def findSolution(rowSolutions, colSolutions, solutionFound, board):
    bL = len(board)
    if bL == 5:
        solutionFound = checkBoard(board, colSolutions)
        if solutionFound:
            return solutionFound
        else:
            return False
    for rowChoices in rowSolutions[bL]:
        board.append(rowChoices)
        boardClone = copy.deepcopy(board)
        solutionFound = findSolution(rowSolutions, colSolutions, solutionFound, boardClone)
        if solutionFound:
            return solutionFound
        board.pop()
    # Backtrack


def nonograms(hints):
    rowSolutions, colSolutions = {}, {}

    for idx in range(len(hints[0])):
        rowSolutions[idx], colSolutions[idx] = [], []

    solutionSet = searchSolutions(len(hints[0]))

    for hintIdx, hint in enumerate(hints[0]):
        validSols = validate(hint, solutionSet)
        colSolutions[hintIdx].extend(validSols)

    for hintIdx, hint in enumerate(hints[1]):
        validSols = validate(hint, solutionSet)
        rowSolutions[hintIdx].extend(validSols)

    for row in rowSolutions:
        print(f'Row: {row} : {rowSolutions[row]}')
    for col in colSolutions:
        print(f'Col: {col} : {colSolutions[col]}')

    rowSolutions = limitSolutions(rowSolutions, colSolutions)

    findSolution(rowSolutions, colSolutions, False, [])
    return answer


clue = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),  # Column Hints
        ((1,), (2,), (3,), (2, 1), (4,)))  # Row Hints

clues15 = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)

tic = time.perf_counter()
r = nonograms(clue)
print(r)
toc = time.perf_counter()

print(f"Time: {toc - tic:0.4f} seconds")

#
# for row in rowSolutions:
#     print(f'Row: {row} : {rowSolutions[row]}')
# for col in colSolutions:
#     print(f'Col: {col} : {colSolutions[col]}')


# Row: 0 : ['00100']
# Row: 1 : ['00011', '11000']
# Row: 2 : ['00111', '01110', '11100']
# Row: 3 : ['11001', '11010']
# Row: 4 : ['01111', '11110']

# Col: 0 : ['00101', '01001', '01010', '10001', '10010', '10100']
# Col: 1 : ['01111', '11110']
# Col: 2 : ['10101']
# Col: 3 : ['00111', '01110', '11100']
# Col: 4 : ['00001', '00010', '00100', '01000', '10000']
