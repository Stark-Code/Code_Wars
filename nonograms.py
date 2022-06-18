class Nonogram:

    def __init__(self, clues):
        self.board = [["." for _ in range(5)] for _ in range(5)]
        self.columnHints = clues[0]
        self.rowHints = clues[1]

    def fill(self, hintIdx, hint, orientation):
        for subHint in hint:
            repeatedPositions = [x for x in range(5)]
            for colIdx in range(len(self.board[hintIdx]) - subHint + 1):
                window = []
                for idx in range(subHint):
                    itemIdx = idx + colIdx
                    if orientation == "rows":
                        if self.board[hintIdx][itemIdx] == ".":
                            window.append(itemIdx)
                    else:
                        if self.board[itemIdx][hintIdx] == "." or self.board[itemIdx][hintIdx] == "1":
                            window.append(itemIdx)
                if len(window) == subHint:
                    for i in repeatedPositions:
                        if i not in window:
                            repeatedPositions.pop(repeatedPositions.index(i))
            for i in repeatedPositions:
                if orientation == "rows":
                    self.board[hintIdx][i] = '1'
                else:
                    self.board[i][hintIdx] = '1'

    def solve(self):
        for hintIdx, hint in enumerate(self.rowHints):
            self.fill(hintIdx, hint, "rows")
        for hintIdx, hint in enumerate(self.columnHints):
            self.fill(hintIdx, hint, "cols")
        for clue in self.columnHints:
            print(clue)
        for row in self.board:
            print(row)

clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)),
         ((1,), (2,), (3,), (2, 1), (4,)))

game = Nonogram(clues)
game.solve()
#
#       1 4 1 3 1
#       1   1
#           1
# 1
# 2
# 3
# 2 1
# 4


# Mark xs
# Search for possible solutions. If there is only one. Fill in values