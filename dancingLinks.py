import time
import copy
import sys

constraints = 4


def buildConstraintsMatrix(cover, bL):
    constraintsMatrix = {}
    lenCover, numConstraints = len(cover), bL * constraints
    numbers = list(range(1, lenCover + 1))
    for y in range(lenCover):
        for x in range(lenCover):
            for num in numbers:
                constraintsMatrix[num, y, x] = [0] * numConstraints

    return constraintsMatrix


# idxOne = 0 - 80, idxTwo = 81 - 161, idxThree = 162 - 242, idxFour = 243 - 323

#  Combined Constraints
def fillConstraintMatrix(constraintMatrix, cover, bL):
    idxOne = 0
    numbers = list(range(1, len(cover[0]) + 1))
    lenNum, lenCover = len(numbers), len(cover)
    for y in range(lenCover):
        idxTwo, idxThree = lenNum * y + bL, 2 * bL
        idxFour = (3 * bL) + (lenNum * 3 * (y // 3))
        for x in range(lenCover):
            idxFour += (lenNum * (x // 3))
            for num in numbers:
                constraintMatrix[num, y, x][idxOne] = 1
                constraintMatrix[num, y, x][idxTwo] = 1
                constraintMatrix[num, y, x][idxThree] = 1
                constraintMatrix[num, y, x][idxFour] = 1
                idxTwo += 1
                idxThree += 1
                idxFour += 1
            idxOne += 1
            idxTwo -= lenNum
            idxFour -= lenNum + (lenNum * (x // 3))

    return constraintMatrix


def coverColumns(cM, uC, key):
    # print("Covering Columns")
    delKeys = []
    for idx in range(len(cM[key])):
        if cM[key][idx] == 1:
            if uC.count(idx) == 1:
                uC.pop(uC.index(idx))
            for row in cM:
                if cM[row][idx] == 1:
                    delKeys.append(row)

    # print(f"Covering row {delKeys}")
    for keys in delKeys:
        if keys in cM:
            del cM[keys]

    # print("Remaining Keys")
    # for remaining in cM:
    #     print(remaining, end=' ')
    # print(f"\nRemaining Unsatisfied Constraints: {uC}")
    return cM, uC


def search(cM, solutionFound, solution, uC):  # cM: constraintsMatrix; uC: unsatisfiedConstraints
    if len(uC) == 0:
        solutionFound = True
        solutionCopy = copy.deepcopy(solution)
        return solutionFound, solutionCopy

    for key in cM:
        if cM[key][uC[0]] == 1:  # uC[0] : constraint
            # print(f"Unsatisfied constraint {uC[0]} found at {key} ")
            solution.append(key)
            cMCopy, uCCopy, solutionCopy = copy.deepcopy(cM), copy.deepcopy(uC), copy.deepcopy(solution)
            cMCovered, uCUpdated = coverColumns(cMCopy, uCCopy, key)
            # print(f"Solution: {solution}")
            solutionFound, solutionCopy = search(cMCovered, solutionFound, solutionCopy, uCUpdated)
            if solutionFound:
                return solutionFound, solutionCopy
            else:
                # print("Continue Loop in Last Stack")
                solution.pop()

    # No Constraints Resolved - Backtrack
    solution.pop()
    return solutionFound, None



def markGivenConstraints(cover, cM, uC):
    for yIdx in range(len(cover)):
        for xIdx in range(len(cover[yIdx])):
            if cover[yIdx][xIdx] != ".":
                key = int(cover[yIdx][xIdx]), yIdx, xIdx
                if key in cM:
                    cM, uC = coverColumns(cM, uC, key)
    return cM, uC


def integrateSolution(cover, solution):
    for constraint in solution:
        cover[constraint[1]][constraint[2]] = constraint[0]
    return cover


def dancingLinks(cover):
    bL = len(cover[0]) * len(cover)  # Number of spots in board
    constraintsMatrix = buildConstraintsMatrix(cover, bL)
    constraintsMatrix = fillConstraintMatrix(constraintsMatrix, cover, bL)
    unsatisfiedConstraints = list(range(0, bL * constraints))
    constraintsMatrix, unsatisfiedConstraints = markGivenConstraints(cover, constraintsMatrix, unsatisfiedConstraints)
    # for key in constraintsMatrix:
    #     print(key, constraintsMatrix[key])
    # print(" ")
    # print(f"Initial unsatisfied constraints: {unsatisfiedConstraints}")
    solutionFound, solution = search(constraintsMatrix, False, [], unsatisfiedConstraints)  # [] : Solution
    # print(f"Solution: {solution}")
    answer = integrateSolution(cover, solution)
    for row in answer:
        print(row)


problem2 = [[".", "."],
            [".", "."]]

sudoku2 = [[".", 2],
           [".", "."]]

problem3 = [[".", ".", "."],
            [".", ".", "."],
            [".", ".", "."]]

sudoku3 = [[2, 3, 1],
           [".", ".", "."],
           [".", ".", "."]]

problem4 = [[".", ".", ".", "."],
            [".", ".", ".", "."],
            [".", ".", ".", "."],
            [".", ".", ".", "."]]

problem5 = [[".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."]]

problem9 = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."], ]

sudoku = [[4, 7, 0, 3, 0, 2, 0, 6, 0], # 152 seconds to solve
          [0, 0, 9, 0, 0, 0, 2, 0, 0],
          [0, 8, 0, 0, 0, 0, 7, 0, 0],
          [0, 5, 0, 0, 1, 9, 0, 0, 0],
          [0, 0, 0, 6, 0, 5, 0, 0, 0],
          [0, 0, 0, 2, 8, 0, 0, 5, 0],
          [0, 0, 3, 0, 0, 0, 0, 9, 0],
          [0, 0, 2, 0, 0, 0, 8, 0, 0],
          [0, 4, 0, 8, 0, 6, 0, 7, 2]]


extreme = [[2, 0, 0, 0, 0, 0, 0, 5, 0],
           [0, 0, 8, 0, 3, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 4, 0, 0, 2, 6, 0],
           [0, 1, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 0, 0, 0, 0, 0],
           [6, 0, 0, 0, 0, 0, 1, 0, 3],
           [4, 0, 0, 5, 0, 9, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 7, 0, 0]]


tic = time.perf_counter()
dancingLinks(extreme)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

# 3x3 Constraint Matrix not being assembled correctly
