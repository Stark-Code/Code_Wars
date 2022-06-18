import sys
import time
import copy

constraints = {  # Idx represent steps from key
    0: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
    1: [[4], [1, 2, 3], [1, 2, 3], [1, 2, 3]],
    2: [[1, 2, 3], [1, 2, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
    3: [[1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4]],
    4: [[1], [2], [3], [4]]
}


class Foundation:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.restrictions = []
        self.value = 0

    def __str__(self):
        return self.value

    @staticmethod
    def intersection(lst1, lst2, lst3, lst4):
        return list(set(lst1) & set(lst2) & set(lst3) & set(lst4))

    def findRestrictions(self, skyscrapers):
        tc = constraints[skyscrapers[0][self.col]][self.row - 1]  # Top
        rc = constraints[skyscrapers[self.row][-1]][4 - self.col]  # Right
        bc = constraints[skyscrapers[-1][self.col]][4 - self.row]  # Bottom
        lc = constraints[skyscrapers[self.row][0]][self.col - 1]  # Left
        self.restrictions = self.intersection(tc, rc, bc, lc)

    def update(self, skyscrapers):
        skyscrapers[self.row][self.col] = self.restrictions[0]  # ?
        return skyscrapers


#  Inference
# def byDefault(skyscrapers: list) -> list:
#     ssCount = [0, 0, 0, 0]
#     for rowIdx in range(1, len(skyscrapers)-1):
#         for colIdx in range(1, len(skyscrapers[rowIdx])-1):
#             if isinstance(skyscrapers[rowIdx][colIdx], int):
#                 ssCount[skyscrapers[rowIdx][colIdx]-1] += 1
#     print(ssCount)
#     return skyscrapers

def printSkyscraper(skyscraper: list) -> None:
    for row in skyscraper:
        temp = []
        for col in row:
            if isinstance(col, Foundation):
                temp.append(col.__str__())
            else:
                temp.append(col)
        print(temp)
    print('')


def buildBlock(clues: list) -> list:
    baseFoundation = ["*", "*", "*", "*"]
    block = [[9, *clues[0], 9]]
    clues[3].reverse()
    for i in range(4):
        block.append([clues[3][i], *baseFoundation, clues[1][i]])
    clues[2].reverse()
    block.append([9, *clues[2], 9])
    return block


def checkWin(skyscrapers):
    for row in skyscrapers:
        for col in row:
            if isinstance(col, Foundation):
                return False
    return True


def checkSight(block, requirement):
    block = list(map(lambda x: 0 if isinstance(x, Foundation) else x, block))
    seen = _max = 0
    for building in block:
        if building > _max:
            seen += 1
            _max = building
    print(f'Seen {seen}, Requirement: {requirement}')
    if seen <= requirement or requirement == 0:  # Might cause problems
        print("Sight requirements met")
        return True
    else:
        # print("Sight requirements not met")
        return False


def checkPlacement(location, value, skyscrapers):
    rowCheck, colCheck = [], []
    print(f'Checking {value} at {location}')
    for i in range(1, 5):  # Check row for repeated values
        rowVal, colVal = skyscrapers[location[0]][i], skyscrapers[i][location[1]]
        if isinstance(rowVal, int):
            rowCheck.append(rowVal)
        if isinstance(colVal, int):
            colCheck.append(colVal)
    if value in rowCheck or value in colCheck:
        return False
    return True


def checkVision(rowIdx, colIdx, skyscrapersClone, value):
    leftBlock = skyscrapersClone[rowIdx][1:5]
    leftBlock[colIdx - 1] = value
    print(f"Checking left with {skyscrapersClone[rowIdx][0]}")
    if not checkSight(leftBlock, skyscrapersClone[rowIdx][0]):  # block: row or column being checked, sight requirement
        return False
    if colIdx == 4:
        leftBlock.reverse()  # Right Block
        print(f"Checking right with {skyscrapersClone[rowIdx][-1]}")
        if not checkSight(leftBlock, skyscrapersClone[rowIdx][-1]):
            return False
    upBlock = [skyscrapersClone[1][colIdx], skyscrapersClone[2][colIdx], skyscrapersClone[3][colIdx],
               skyscrapersClone[4][colIdx]]
    upBlock[rowIdx-1] = value
    # print(f'Upblock: {upBlock}')
    # print(f'Value: {value}')
    # print(f'ColIdx: {colIdx}')
    # print(f'Checking up with {skyscrapersClone[0][colIdx]}')
    if not checkSight(upBlock, skyscrapersClone[0][colIdx]):
        return False
    if rowIdx == 4:
        upBlock.reverse()
        print(f'Checking down with {skyscrapersClone[-1][colIdx]}')
        if not checkSight(upBlock, skyscrapersClone[-1][colIdx]):
            return False
    return True


def recursiveSearch(skyscrapers):
    print("Recursive Search")
    printSkyscraper(skyscrapers)
    if checkWin(skyscrapers):
        print(skyscrapers)
        return skyscrapers, True
    skyscrapersClone = copy.deepcopy(skyscrapers)
    for rowIdx in range(1, len(skyscrapersClone) - 1):
        for colIdx in range(1, len(skyscrapersClone[rowIdx]) - 1):
            ss = skyscrapersClone[rowIdx][colIdx]
            if isinstance(ss, Foundation):
                print(f'Next skyscraper location found at {rowIdx, colIdx}')
                while ss.restrictions:
                    print(f'Restrictions: {ss.restrictions}')
                    if checkPlacement([rowIdx, colIdx], ss.restrictions[-1], skyscrapers) and \
                            checkVision(rowIdx, colIdx, skyscrapersClone, ss.restrictions[-1]):
                        print(f'{ss.restrictions[-1]} being added')
                        skyscrapersClone[rowIdx][colIdx] = ss.restrictions[-1]
                        ss.restrictions.pop()
                        result, gameOver = recursiveSearch(skyscrapersClone)
                        if gameOver:
                            return result, gameOver
                    else:
                        ss.restrictions.pop()
                return 0, False


def solve_puzzle(c: tuple) -> tuple:
    n = len(c) // 4
    clues = [list(c[i:i + n]) for i in range(0, len(c), n)]  # Top, Right, Bottom, Left
    skyscrapers = buildBlock(clues)
    printSkyscraper(skyscrapers)
    for rowIdx, row in enumerate(skyscrapers):  # Find Constraints
        for colIdx, col in enumerate(row):
            if col == "*":
                ss = Foundation(rowIdx, colIdx)
                skyscrapers[rowIdx][colIdx] = ss
                ss.findRestrictions(skyscrapers)
                if len(ss.restrictions) == 1:
                    skyscrapers = ss.update(skyscrapers)  # Fill
    result, gameOver = recursiveSearch(skyscrapers)
    return tuple(result[1][1:5]), tuple(result[2][1:5]), tuple(result[3][1:5]), tuple(result[4][1:5])


clue1 = (2, 2, 1, 3,
         2, 2, 3, 1,
         1, 2, 2, 3,
         3, 2, 1, 3)

clue2 = (2, 3, 2, 1,
         1, 4, 2, 2,
         3, 2, 1, 2,
         3, 1, 2, 3)

clue3 = (0, 0, 1, 2,
         0, 2, 0, 0,
         0, 3, 0, 0,
         0, 1, 0, 0)

clue4 = (1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1)

'''
[9, 2, 2, 1, 3, 9]
[3, 1, 3, 4, 2, 2] 
[1, 4, 2, 1, 3, 2]
[2, 3, 4, 2, 1, 3]
[3, 2, 1, 3, 4, 1]
[9, 3, 2, 2, 1, 9]
'''

tic = time.perf_counter()
r = solve_puzzle(clue4)
print(r)
# printSkyscraper(r)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

'''
[9, 2, 2, 1, 3, 9]
[3, 0, 0, 4, 0, 2]       
[2, 0, 4, 0, 0, 2]       
[1, 4, 0, 0, 0, 3]       
[3, 0, 0, 0, 4, 1]       
[9, 3, 2, 2, 1, 9]
'''

'''
[9, 0, 0, 1, 2, 9]
[0,  ,  , 4,  , 0]
[0,  ,  ,  ,  , 2]
[1, 4,  ,  ,  , 0]
[0,  ,  ,  ,  , 0]
[9, 0, 0, 3, 0, 9]
'''