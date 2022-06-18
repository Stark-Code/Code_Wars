import copy
import time


def incGridSize(cells):
    newCells = [[0 for _ in range(len(cells[0])+2)]]
    for row in cells:
        newCells.append([0, *row, 0])
    newCells.append([0 for _ in range(len(cells[0])+2)])
    return newCells


def findNeighbors(cellLoc, cells):
    neighborCount = 0
    for searchPos in [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]:
        searchSquare = [cellLoc[0]+searchPos[0], cellLoc[1]+searchPos[1]]
        if 0 <= searchSquare[0] < len(cells) and 0 <= searchSquare[1] < len(cells[0]):
            if cells[searchSquare[0]][searchSquare[1]] == 1:
                neighborCount += 1
    return neighborCount


def cycleCells(location, neighborCount, cells, cellsClone):
    if cells[location[0]][location[1]] == 0:
        if neighborCount == 3:
            cellsClone[location[0]][location[1]] = 1
    elif neighborCount not in [2, 3]:
        cellsClone[location[0]][location[1]] = 0
    return cellsClone


def growBorder(cells):
    for col in cells[0]:
        if col == 1: return True
    for row in range(1, len(cells)-1):
        if cells[row][0] == 1 or cells[row][-1] == 1: return True
    for col in cells[-1]:
        if col == 1: return True
    return False


def trimBorder(cells):
    trim = True
    while trim:
        trim = False
        for col in cells[0]:
            if col == 1: break
        else:
            cells.pop(0)
            trim = True

        for col in cells[-1]:
            if col == 1: break
        else:
            cells.pop()
            trim = True

        for row in range(0, len(cells)):
            if cells[row][0] == 1: break
        else:
            for row in range(0, len(cells)):
                cells[row].pop(0)
                trim = True

        for row in range(0, len(cells)):
            if cells[row][-1] == 1: break
        else:
            for row in range(0, len(cells)):
                cells[row].pop()
                trim = True
    return cells


def get_generation(cells, generations):
    growthCycle = 0
    cells = incGridSize(cells)
    while growthCycle < generations:
        cellsClone = copy.deepcopy(cells)
        for rowIdx, row in enumerate(cells):
            for colIdx, col in enumerate(row):
                neighbors = findNeighbors((rowIdx, colIdx), cells)
                cellsClone = cycleCells((rowIdx, colIdx), neighbors, cells, cellsClone)
        if growBorder(cellsClone):
            cells = incGridSize(cellsClone)
        else:
            cells = cellsClone
        growthCycle += 1
    cells = trimBorder(cells)
    return cells

start = [[1, 0, 0],
         [0, 1, 1],
         [1, 1, 0]]

# end   = [[0,1,0],
#          [0,0,1],
#          [1,1,1]]

'''
Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
Any live cell with more than three live neighbours dies, as if by overcrowding.
Any live cell with two or three live neighbours lives on to the next generation.
Any dead cell with exactly three live neighbours becomes a live cell.
'''

tic = time.perf_counter()
r = get_generation(start, 1)
for _row in r:
    print(_row)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")