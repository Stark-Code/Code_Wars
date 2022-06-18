import copy

global answer

class Nonogram:

    def __init__(self, hints):
        self.hints = hints

    def validate(self, hint, solList):
        # print(f"Hint: {hint}")
        validSolutions = []
        for solution in solList:
            # print(f'Checking {solution}')

            hintStructure = []
            clueLen = 0
            for idx, item in enumerate(solution):
                if item == "1":
                    clueLen += 1
                if item == "0" or idx == len(solution) - 1:
                    if clueLen > 0:
                        hintStructure.append(clueLen)
                        clueLen = 0
            if tuple(hintStructure) == hint:
                validSolutions.append(solution)
        return validSolutions

    def incrementStrSolution(self, solution):
        solution += 1
        return solution, "{0:05b}".format(solution)

    def searchSolutions(self, bS):
        solution, strSols, limit = 0, [], "1" * bS
        while True:
            solution, strSol = self.incrementStrSolution(solution)
            strSols.append(strSol)
            if strSol == limit:
                break
        return strSols

    def limitSolutions(self, rowSolutions, colSolutions):
        for col in colSolutions:
            if len(colSolutions[col]) == 1:
                for idx in range(len(colSolutions[col][0])):
                    removals = []
                    for solIdx, sol in enumerate(rowSolutions[idx]):
                        if sol[col] != colSolutions[col][0][idx]:
                            removals.append(rowSolutions[idx][solIdx])
                    for remove in removals:
                        rowSolutions[idx].pop(rowSolutions[idx].index(remove))

        return rowSolutions

    def checkBoard(self, board, colSolutions):
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

    def findSolution(self, rowSolutions, colSolutions, solutionFound, board):
        bL = len(board)
        if bL == 5:
            solutionFound = self.checkBoard(board, colSolutions)
            if solutionFound:
                return solutionFound
            else:
                return False
        for rowChoices in rowSolutions[bL]:
            board.append(rowChoices)
            boardClone = copy.deepcopy(board)
            solutionFound = self.findSolution(rowSolutions, colSolutions, solutionFound, boardClone)
            if solutionFound:
                return solutionFound
            board.pop()
        # Backtrack

    def solve(self):
        hints = self.hints
        rowSolutions, colSolutions = {}, {}

        for idx in range(len(hints[0])):
            rowSolutions[idx], colSolutions[idx] = [], []

        solutionSet = self.searchSolutions(len(hints[0]))

        for hintIdx, hint in enumerate(hints[0]):
            validSols = self.validate(hint, solutionSet)
            colSolutions[hintIdx].extend(validSols)

        for hintIdx, hint in enumerate(hints[1]):
            validSols = self.validate(hint, solutionSet)
            rowSolutions[hintIdx].extend(validSols)

        rowSolutions = self.limitSolutions(rowSolutions, colSolutions)

        self.findSolution(rowSolutions, colSolutions, False, [])
        re = []
        bs = []
        for a in answer:
            temp = []
            for x in a:
                temp.append(int(x))
            re.append(temp)
        for y in re:
            bs.append(tuple(y))
        return bs

clue = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),  # Column Hints
        ((1,), (2,), (3,), (2, 1), (4,)))  # Row Hints

clue2 = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),  # Column Hints
         ((1,), (2,), (1, 3), (2, 2), (4,)))  # Row Hints

nonogram = Nonogram(clue)
r = nonogram.solve()
print(r)
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
