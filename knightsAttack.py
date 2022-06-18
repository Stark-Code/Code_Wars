import time
from colorama import init, Back

init(autoreset=True)
print(Back.RED + '*************************************')


def insertionSort(_list, node):
    _list.append(node)
    # print(f'List Length: {len(_list)}')
    # print('Unsorted List')
    # for node in _list: print(node.fCost)
    if len(_list) == 1: return _list
    idx = -2
    while _list[idx+1].fCost < _list[idx].fCost:
        _list[idx+1], _list[idx] = _list[idx], _list[idx+1]
        idx -= 1
        # print(f'Idx: {idx}')
        if abs(idx) == len(_list): break
    # print('Sorted List')
    # for node in _list: print(node.fCost)
    # print('\n')
    return _list

#
# class Node:
#     def __init__(self, pos):
#         self.pos = pos
#         self.gCost = None
#         self.hCost = None
#         self.fCost = None
#         self.closed = False
#         self.parent = None
#
#
# def printMap(start, dest, obstacles):
#     hMax, hMin = max(start[0], dest[0]), min(start[0], dest[0])
#     wMax, wMin = max(start[1], dest[1]), min(start[1], dest[1])
#     for o in obstacles:
#         if o[0] > hMax: hMax = o[0]
#         if o[1] > wMax: wMax = o[1]
#         if o[0] < hMin: hMin = o[0]
#         if o[1] < wMin: wMin = o[1]
#     print(f'Height: {hMax}, Width: {wMax}')
#     grid = [['.' for x in range(wMax + 10)] for y in range(hMax + 10)]
#
#     # for row in grid:
#     #     print(row)
#     for o in obstacles:
#         grid[o[0]][o[1]] = 'x'
#     grid[start[0]][start[1]] = 's'
#     grid[dest[0]][dest[1]] = 'd'
#     for row in grid:
#         print(row)
#
#
# def calculateCosts(parentNode, childNode, destination):
#     childNode.gCost = parentNode.gCost + 1
#     childNode.hCost = (abs(destination[0] - childNode.pos[0]) + abs(destination[1] - childNode.pos[1]))
#     childNode.fCost = childNode.hCost + childNode.gCost
#
#
# def knightMoves(currPos, obDict, seen):
#     moves = []
#     for move in [[-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]:
#         movement = (currPos[0] + move[0], currPos[1] + move[1])
#         if movement in seen: continue
#         if movement[0] in obDict:
#             if movement[1] not in obDict[movement[0]]:
#                 moves.append(movement)
#         else:
#             moves.append(movement)
#     return moves
#
#
# def evaluateNodePriority(nodeTracker):
#     min_F_Cost = float('Inf')
#     minNode = None
#     nodeTracker.sort(key = lambda node: node.fCost)
#     for node in nodeTracker:
#         if node.closed: continue
#         else: minNode = node
#         if node.fCost < min_F_Cost:
#             minNode = node
#             min_F_Cost = node.fCost
#         elif node.fCost == min_F_Cost:
#             if node.hCost < minNode.hCost:
#                 minNode = node
#     if not minNode:
#         return None
#     minNode.closed = True
#     # nodeTracker.pop(nodeTracker.index(minNode))
#     return minNode
#
#
# def addBorder(start, dest, obstacles):
#     '''
#         At hMin-1 and hMin-2 from wMin to wMax add tuple (curr_H_Min, currW)
#         At hMax+1 and hMax+2 from wMin to wMax add tuple (curr_H_Min, currW)
#         At wMin-1 and wMin-2 from hMin to hMax add tuple (curr_H, curr_W_Min)
#         At wMax+1 and wMax+2 from hMin to hMax add tuple (curr_H, curr_W_Max)
#         '''
#     hMax, hMin = max(start[0], dest[0]), min(start[0], dest[0])
#     wMax, wMin = max(start[1], dest[1]), min(start[1], dest[1])
#     for o in obstacles:
#         if o[0] > hMax: hMax = o[0]
#         if o[1] > wMax: wMax = o[1]
#         if o[0] < hMin: hMin = o[0]
#         if o[1] < wMin: wMin = o[1]
#     for yIdx in range(hMin-5, hMax+5):  # Prints Columns
#         obstacles.append((yIdx, wMin-5))  # Left Columns
#         obstacles.append((yIdx, wMin-6))
#         obstacles.append((yIdx, wMax + 5))  # Right Columns
#         obstacles.append((yIdx, wMax + 6))
#     for xIdx in range(wMin-6, wMax+7):  # Prints rows
#         obstacles.append((hMin-5, xIdx))  # Top rows
#         obstacles.append((hMin-6, xIdx))
#         obstacles.append((hMax+5, xIdx))  # Bottom rows
#         obstacles.append((hMax+6, xIdx))
#
#     return tuple(obstacles)
#
#
# def attack(start, dest, obstacles):
#     # printMap(start, dest, obstacles)
#     obstacles = addBorder(start, dest, list(obstacles))
#     # printMap(start, dest, obstacles)
#     obDict = {}
#     nodeTracker = []
#     seen = {}
#     currNode = Node(start)
#     currNode.hCost, currNode.gCost, currNode.fCost, currNode.closed, currNode.parent = 0, 0, 0, True, 'Origin'
#     for t in obstacles:  # Hash obstacles list
#         if t[0] not in obDict:
#             obDict[t[0]] = [t[1]]
#         else:
#             obDict[t[0]].append(t[1])
#     reachable = knightMoves(dest, obDict, seen)
#     if len(reachable) == 0: return None
#     while currNode.pos != dest:
#         # print(currNode.pos)
#         kMoves = knightMoves(currNode.pos, obDict, seen)
#         # print(f'Knight at position {currNode.pos}')
#         # print(f'Available moves: {kMoves}')
#         for move in kMoves:
#             seen[move] = 'x'
#             newNode = Node(move)
#             calculateCosts(currNode, newNode, dest)
#             newNode.parent = currNode
#             nodeTracker.append(newNode)
#             # nodeTracker = insertionSort(nodeTracker, newNode)
#         currNode = evaluateNodePriority(nodeTracker)
#         # print(f'{currNode.pos}, {currNode.hCost}. Destination: {dest}')
#         if currNode is None:
#             print('No path available')
#             return None
#     steps = 0
#     while currNode.parent != 'Origin':
#         currNode = currNode.parent
#         steps += 1
#     print(f'Steps: {steps}')
#     return steps




class Node:
    def __init__(self, pos):
        self.pos = pos
        self.gCost = None
        self.hCost = None
        self.fCost = None
        self.closed = False
        self.parent = None


def printMap(start, dest, obstacles):
    hMax, hMin = max(start[0], dest[0]), min(start[0], dest[0])
    wMax, wMin = max(start[1], dest[1]), min(start[1], dest[1])
    for o in obstacles:
        if o[0] > hMax: hMax = o[0]
        if o[1] > wMax: wMax = o[1]
        if o[0] < hMin: hMin = o[0]
        if o[1] < wMin: wMin = o[1]
    print(f'Height: {hMax}, Width: {wMax}')
    grid = [['.' for x in range(wMax + 10)] for y in range(hMax + 10)]

    # for row in grid:
    #     print(row)
    for o in obstacles:
        grid[o[0]][o[1]] = 'x'
    grid[start[0]][start[1]] = 's'
    grid[dest[0]][dest[1]] = 'd'
    for row in grid:
        print(row)


def calculateCosts(parentNode, childNode, destination):
    childNode.gCost = parentNode.gCost + .1
    childNode.hCost = (abs(destination[0] - childNode.pos[0]) + abs(destination[1] - childNode.pos[1]))
    childNode.fCost = childNode.hCost + childNode.gCost


def knightMoves(currPos, obDict, seen):
    moves = []
    for move in [[-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2]]:
        movement = (currPos[0] + move[0], currPos[1] + move[1])
        if movement in seen: continue
        if movement[0] in obDict:
            if movement[1] not in obDict[movement[0]]:
                moves.append(movement)
        else:
            moves.append(movement)
    return moves


def evaluateNodePriority(nodeTracker):
#     min_F_Cost = float('Inf')
#     nodeTracker.sort(key = lambda node: node.fCost)
    minNode = None
    for node in nodeTracker:
        if node.closed: continue
        else:
            minNode = node
            break
#         if node.fCost < min_F_Cost:
#             minNode = node
#             min_F_Cost = node.fCost
#         elif node.fCost == min_F_Cost:
#             if node.hCost < minNode.hCost:
#                 minNode = node
    if not minNode:
        return None
    minNode.closed = True
    nodeTracker.pop(nodeTracker.index(minNode))
    return minNode


def addBorder(start, dest, obstacles):
    '''
        At hMin-1 and hMin-2 from wMin to wMax add tuple (curr_H_Min, currW)
        At hMax+1 and hMax+2 from wMin to wMax add tuple (curr_H_Min, currW)
        At wMin-1 and wMin-2 from hMin to hMax add tuple (curr_H, curr_W_Min)
        At wMax+1 and wMax+2 from hMin to hMax add tuple (curr_H, curr_W_Max)
        '''
    hMax, hMin = max(start[0], dest[0]), min(start[0], dest[0])
    wMax, wMin = max(start[1], dest[1]), min(start[1], dest[1])
    for o in obstacles:
        if o[0] > hMax: hMax = o[0]
        if o[1] > wMax: wMax = o[1]
        if o[0] < hMin: hMin = o[0]
        if o[1] < wMin: wMin = o[1]
    for yIdx in range(hMin-5, hMax+5):  # Prints Columns
        obstacles.append((yIdx, wMin-5))  # Left Columns
        obstacles.append((yIdx, wMin-6))
        obstacles.append((yIdx, wMax + 5))  # Right Columns
        obstacles.append((yIdx, wMax + 6))
    for xIdx in range(wMin-6, wMax+7):  # Prints rows
        obstacles.append((hMin-5, xIdx))  # Top rows
        obstacles.append((hMin-6, xIdx))
        obstacles.append((hMax+5, xIdx))  # Bottom rows
        obstacles.append((hMax+6, xIdx))

    return tuple(obstacles)


def attack(start, dest, obstacles):
#     print(start, dest, obstacles)
    # printMap(start, dest, obstacles)
    obstacles = addBorder(start, dest, list(obstacles))
    # printMap(start, dest, obstacles)
    obDict = {}
    nodeTracker = []
    seen = {}
    currNode = Node(start)
    currNode.hCost, currNode.gCost, currNode.fCost, currNode.closed, currNode.parent = 0, 0, 0, True, 'Origin'
    for t in obstacles:  # Hash obstacles list
        if t[0] not in obDict:
            obDict[t[0]] = [t[1]]
        else:
            obDict[t[0]].append(t[1])
    reachable = knightMoves(dest, obDict, seen)
    if len(reachable) == 0: return None
    while currNode.pos != dest:
#         print(currNode.pos)
        kMoves = knightMoves(currNode.pos, obDict, seen)
        # print(f'Knight at position {currNode.pos}')
        # print(f'Available moves: {kMoves}')
        for move in kMoves:
            seen[move] = 'x'
            newNode = Node(move)
            calculateCosts(currNode, newNode, dest)
            newNode.parent = currNode
            nodeTracker = insertionSort(nodeTracker, newNode)
            nodeTracker.append(newNode)
        currNode = evaluateNodePriority(nodeTracker)
        if currNode is None:
            print('No path available')
            return None
    steps = 0
    while currNode.parent != 'Origin':
        currNode = currNode.parent
        steps += 1
#     print(f'Steps: {steps}')
    return steps



tic = time.perf_counter()
# attack((7, 1), (3, 3), ((5, 1), (5, 2), (5, 0), (4, 2), (4, 4), (7, 5)))  # Result : 4
# attack((0, 0), (7, 7), ((5, 6), (5, 8), (6, 5), (6, 9), (9, 6), (8, 5), (8, 9), (9, 8)))
attack((-200, 214), (135, -121), ())
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

s = (2, 4)
d = (3, 55)
obst = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (0, 24), (0, 25), (0, 26), (0, 27), (0, 28), (0, 29), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (0, 39), (0, 40), (0, 41), (0, 42), (0, 43), (0, 44), (0, 45), (0, 46), (0, 47), (0, 48), (0, 49), (0, 50), (0, 51), (0, 52), (0, 53), (0, 54), (0, 55), (0, 56), (0, 57), (0, 58), (0, 59), (0, 60), (0, 61), (0, 62), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30), (1, 31), (1, 32), (1, 33), (1, 34), (1, 35), (1, 36), (1, 37), (1, 38), (1, 39), (1, 40), (1, 41), (1, 42), (1, 43), (1, 44), (1, 45), (1, 46), (1, 47), (1, 48), (1, 49), (1, 50), (1, 51), (1, 52), (1, 53), (1, 54), (1, 55), (1, 56), (1, 57), (1, 58), (1, 59), (1, 60), (1, 61), (1, 62), (2, 0), (2, 1), (2, 61), (2, 62), (3, 0), (3, 1), (3, 61), (3, 62), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (4, 25), (4, 26), (4, 27), (4, 28), (4, 29), (4, 30), (4, 31), (4, 32), (4, 33), (4, 34), (4, 35), (4, 36), (4, 37), (4, 38), (4, 39), (4, 40), (4, 41), (4, 42), (4, 43), (4, 44), (4, 45), (4, 46), (4, 47), (4, 48), (4, 49), (4, 50), (4, 51), (4, 52), (4, 53), (4, 54), (4, 55), (4, 56), (4, 57), (4, 58), (4, 59), (4, 60), (4, 61), (4, 62), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (5, 30), (5, 31), (5, 32), (5, 33), (5, 34), (5, 35), (5, 36), (5, 37), (5, 38), (5, 39), (5, 40), (5, 41), (5, 42), (5, 43), (5, 44), (5, 45), (5, 46), (5, 47), (5, 48), (5, 49), (5, 50), (5, 51), (5, 52), (5, 53), (5, 54), (5, 55), (5, 56), (5, 57), (5, 58), (5, 59), (5, 60), (5, 61), (5, 62))
# attack(s, d, obst)
