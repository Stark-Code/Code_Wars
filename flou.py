import copy
import sys
import itertools
import border


def printGrid(grid):
    for row in grid:
        print(row)


def findBlocks(grid):
    blockLocations = []
    for yIdx, y in enumerate(grid):
        for xIdx, x in enumerate(y):
            if x == 'B':
                blockLocations.append((yIdx, xIdx))
    return blockLocations


def checkSolution(grid):
    for row in grid:
        for col in row:
            if col == '.':
                return False
    return True


def fillGrid(blockLocations, blockIdx, directionIdx, grid) -> list:  # Checked arg values, look ok
    directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    legalMoves = True
    y, x = blockLocations[blockIdx][0] + directions[directionIdx][0], blockLocations[blockIdx][1] + \
        directions[directionIdx][1]

    while legalMoves:
        if directionIdx == 0: print(f"Checking {blockLocations[blockIdx]} for upward marks")
        if directionIdx == 1: print(f"Checking {blockLocations[blockIdx]} for rightward marks")
        if directionIdx == 2: print(f"Checking {blockLocations[blockIdx]} for downward marks")
        if directionIdx == 3: print(f"Checking {blockLocations[blockIdx]} for leftward marks")
        legalMoves = False
        while grid[y][x] == '.':
            print(f'{(y, x)} marked')
            # print(f'y: {y}, x: {x}')
            legalMoves = True
            grid[y][x] = 'B'
            y += directions[directionIdx][0]
            x += directions[directionIdx][1]
        y -= directions[directionIdx][0]  # Bad programming
        x -= directions[directionIdx][1]
        if legalMoves:
            if directionIdx == 3:
                directionIdx = 0
            else:
                directionIdx += 1
            y, x = y + directions[directionIdx][0], x + directions[directionIdx][1]
            # print(f'Last: y: {y}, x: {x}')
    return grid

dirList = ['Up', 'Right', 'Down', 'Left']

def recursiveDFS(blockLocations, blockIdx, grid, result):
    print('Recursive Search Call')
    gridCopy = copy.deepcopy(grid)
    blockIdxCopy = copy.copy(blockIdx)
    for directionIdx, direction in enumerate([[-1, 0], [0, 1], [1, 0], [0, -1]]):
        if grid[blockLocations[blockIdx][0] + direction[0]][blockLocations[blockIdx][1] + direction[1]] == '.':
            grid = fillGrid(blockLocations, blockIdx, directionIdx, grid)
            result[blockIdx] = [*blockLocations[blockIdx], dirList[blockIdx]]
            printGrid(grid)
            if checkSolution(grid) and blockIdx == len(blockLocations)-1:  # Off by 1 error?
                return grid, True, result  # grid, Solution_Found
            if blockIdx < len(blockLocations)-1:
                blockIdxCopy += 1
            grid, solutionFound, result = recursiveDFS(blockLocations, blockIdxCopy, grid, result)
            if solutionFound:
                return grid, solutionFound, result
            else:  # Backtracking
                print('No available solutions with current direction. Trying next direction')
                grid = gridCopy
                blockIdxCopy = copy.copy(blockIdx)
            grid = gridCopy
            # Reset blockIdxCopy here too?2222222222222222222222222222222222222222222222222222222222222222222222222222
    print("No Solution - Backtrack")
    return grid, False, result


def play_flou(game_map):
    grid = [[x for x in y] for y in game_map.split('\n')]
    blockLocations = findBlocks(grid)
    result = [[] for x in range(len(blockLocations))]
    print(blockLocations)
    for blockLocationP in itertools.permutations(blockLocations):
        solution, solutionFound, result = recursiveDFS(blockLocationP, 0, grid, result)
        if solutionFound:
            print(solution)
            print('Solution')
            print(result)
            break
    print('Finished')
    return result
game_map1 = '''+----+
|B...|
|....|
|....|
|...B|
+----+'''

game_map2 = '''+----+
|....|
|...B|
|.B..|
|B...|
+----+'''

game_map2 = '''+-----+
|.....|
|.B.B.|
|.B...|
|.....|
|...B.|
+-----+'''

border.printBorder()
play_flou(game_map2)
