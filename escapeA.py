import time
import sys
from colorama import init, Back
init(autoreset=True)


orientationCode = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

directionDict = {
    '^': {  # (-1, 0)
        (-2, 0): [['F'], '^'],
        (-1, 1): [['R', 'F'], '>'],
        (0, 0): [['B', 'F'], 'v'],
        (-1, -1): [['L', 'F'], '<']},
    '>': {  # (0, 1)
        (-1, 1): [['L', 'F'], '^'],
        (0, 2): [['F'], '>'],
        (1, 1): [['R', 'F'], 'v'],
        (0, 0): [['B', 'F'], '<']},
    'v': {  # (1, 0)
        (0, 0): [['B', 'F'], '^'],
        (1, 1): [['L', 'F'], '>'],
        (2, 0): [['F'], 'v'],
        (1, -1): [['R', 'F'], '<']},
    '<': {  # (0, -1)
        (-1, -1): [['R', 'F'], '^'],
        (0, 0): [['B', 'F'], '>'],
        (1, -1): [['L', 'F'], 'v'],
        (0, -2): [['F'], '<']}
}



class Node:
    def __init__(self, position):
        self.position = position
        self.gCost = None  # distance from starting node
        self.hCost = None  # distance from exit node
        self.fCost = None  # gCost + hCost
        self.closed = False  # Explored node gets closed
        self.parent = None

    def __str__(self):
        if self.gCost is None:
            return '-'
        else:
            return str(self.gCost)


def drawMaze(maze):
    for y in maze:
        temp = []
        for x in y:
            if isinstance(x, Node): temp.append(x.__str__())
            else: temp.append(x)
        print(temp)
    print('')


def findPlayer(maze):
    for yIdx, y in enumerate(maze):
        for xIdx, x in enumerate(y):
            if x in ['^', 'v', '>', '<']:
                return (yIdx, xIdx), x


def findExits(maze):
    exits, lastRow, lastCol = [], len(maze) - 1, len(maze[0]) - 1
    for xIdx, x in enumerate(maze[0]):
        if x != '#': exits.append((0, xIdx))
    for yIdx in range(1, lastRow):
        if maze[yIdx][0] != '#': exits.append((yIdx, 0))
        if maze[yIdx][lastCol] != '#': exits.append((yIdx, lastCol))
    for xIdx, x in enumerate(maze[lastRow]):
        if x != '#': exits.append((lastRow, xIdx))
    return exits


def calculateCosts(parentNode, maze, _exit):  # Evaluates the neighboring nodes g, h, and f costs
    nodeTracker = []
    for searchPos in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        searchSquare = (parentNode.position[0] + searchPos[0], parentNode.position[1] + searchPos[1])
        if isinstance(maze[searchSquare[0]][searchSquare[1]], Node):
            adjNode = maze[searchSquare[0]][searchSquare[1]]
            if adjNode.fCost is None:
                adjNode.gCost = parentNode.gCost + 1
                adjNode.hCost = abs(_exit[0] - searchSquare[0]) + abs(_exit[1] - searchSquare[1])
                adjNode.fCost = adjNode.hCost + adjNode.gCost
                adjNode.parent = parentNode
                nodeTracker.append(adjNode)
            elif parentNode.gCost + 1 < adjNode.gCost:
                sys.exit("Returned to Neighbor!")
    return nodeTracker


def evaluateNodePriority(nodeTracker):
    min_F_Cost = float('Inf')
    minNode = None
    for node in nodeTracker:
        if node.closed: continue
        if node.fCost < min_F_Cost:
            minNode = node
            min_F_Cost = node.fCost
        elif node.fCost == min_F_Cost:
            if node.hCost < minNode.hCost:
                minNode = node
    if not minNode:
        return None
    minNode.closed = True
    return minNode


def getDirectionsToExit(orientation, parentNode, startNode, _exit):
    dirList = []
    movements = []
    while parentNode.gCost != 0:
        print(parentNode.position)
        dirList.append(parentNode.position)
        parentNode = parentNode.parent
    dirList.append(startNode.position)
    dirList.reverse()
    print(dirList)
    for posIdx, pos in enumerate(dirList):
        if posIdx == len(dirList)-1: break
        searchPos = [dirList[posIdx+1][0] - dirList[posIdx][0], dirList[posIdx+1][1] - dirList[posIdx][1]]
        orientationNumeric = orientationCode[orientation]
        directionMod = (searchPos[0] + orientationNumeric[0], searchPos[1] + orientationNumeric[1])
        movements.extend(directionDict[orientation][directionMod][0])
        orientation = directionDict[orientation][directionMod][1]
    print(movements)
    return movements
    # Calculate search position by finding abs diff between nodes x and y
    # get orientation numeric via players current orientation and dictionary
    # Calc directionMod = (searchPos[0] + orientationNumeric[0], searchPos[1] + orientationNumeric[1])
    # Get directionDict[player.orientation][directionMod]


def bfs(node, maze, _exit, nodeTracker):
    while node.position != _exit:
        drawMaze(maze)
        nodeTracker.extend(calculateCosts(node, maze, _exit))
        node = evaluateNodePriority(nodeTracker)
        if not node:
            return None
    drawMaze(maze)
    print(len(nodeTracker))
    print(f'Exit Found. NodePos: {node.position}, _exit: {_exit}')
    return node



def escape(maze):
    maze = [[Node((yIdx, xIdx)) if x == ' ' else x for xIdx, x in enumerate(y)] for yIdx, y in enumerate(maze)]
    start, orientation = findPlayer(maze)
    startNode = Node(start)
    startNode.hCost, startNode.gCost, startNode.fCost, startNode.closed = 0, 0, 0, True
    maze[startNode.position[0]][startNode.position[1]] = startNode
    exits = findExits(maze)
    if len(exits) == 0:
        return []
    exits.sort(key=lambda _exit: abs(startNode.position[0] - _exit[0]) + abs(startNode.position[1] - _exit[1]))
    for _exit in exits:
        endNode = bfs(startNode, maze, _exit, nodeTracker=[])
        if endNode: break
    else:
        return []
    return getDirectionsToExit(orientation, endNode, startNode, exits[0])


maze1 = [
    '###########',
    '##        #',
    '#   ##### #',
    '# ### #  ##',
    '# # #^## # ',
    '# # # # # #',
    '#       # #',
    '###########'
]

maze2 = ["#########################################",
         "#  <   #       #     #         # #   #   #",
         "##### # ##### # ### # # ##### # # # ### #",
         "# #   #   #   #   #   # #     #   #   # #",
         "# # # ### # ########### # ####### # # # #",
         "#   #   # # #       #   # #   #   # #   #",
         "####### # # # ##### # ### # # # #########",
         "#   #     # #     # #   #   # # #       #",
         "# # ####### ### ### ##### ### # ####### #",
         "# #             #   #     #   #   #   # #",
         "# ############### ### ##### ##### # # # #",
         "#               #     #   #   #   # #   #",
         "##### ####### # ######### # # # ### #####",
         "#   # #   #   # #         # # # #       #",
         "# # # # # # ### # # ####### # # ### ### #",
         "# # #   # # #     #   #     # #     #   #",
         "# # ##### # # ####### # ##### ####### # #",
         "# #     # # # #   # # #     # #       # #",
         "# ##### ### # ### # # ##### # # ### ### #",
         "#     #     #     #   #     #   #   #    ",
         "#########################################"]

maze3 = [
    '#####################',
    '      # #     #     #',
    '##### # # ### # ### #',
    '#   # # #   # # #   #',
    '# # # # ##### # ### #',
    '# #   # #     # #   #',
    '# # ### # ##### # ###',
    '# #       #     # # #',
    '# ##### ### ### # # #',
    '#   # # #   #   # # #',
    '### # # # ### ### # #',
    '#   #   # # #   # # #',
    '# ####### # ##### # #',
    '# #   #       #     #',
    '# # # # ##### # #####',
    '#   # #   #   # #   #',
    '##### ### ##### ### #',
    '#     # #   #   #   #',
    '# ##### ### # ### ###',
    '# # #     # #       #',
    '# # # ### ######### #',
    '#   #   #           #',
    '# # ### ########### #',
    '# # #   #           #',
    '# ### ### ###########',
    '# #   #   #     #   #',
    '# # ### ### ### # # #',
    '# #   #   # #     # #',
    '# ### ### # # # #####',
    '#   #   #   # # #   #',
    '# # ########### # # #',
    '# #           # # # #',
    '# ########### # # # #',
    '#   #     #       # #',
    '##### # ### ####### #',
    '#     #   # # #     #',
    '### # ### # # # #####',
    '#   # #   #   #     #',
    '# ### ############# #',
    '# #   #         #   #',
    '# # ### ####### # # #',
    '# # # #   #     # # #',
    '# # # ### # ##### # #',
    '# #   #   #       # #',
    '##### # ########### #',
    '#     #     #       #',
    '# ########### ##### #',
    '# #         # #     #',
    '# # ####### # # #####',
    '#   #   #   # #     #',
    '### # # # ### # ### #',
    '#   # #   #   # #   #',
    '# ############# # ###',
    '# #   #   #     #   #',
    '# # # # ### ####### #',
    '# # #   #   # #     #',
    '# # ### # # # # #####',
    '# #   #   # # #     #',
    '# ### ##### # ##### #',
    '# #   # #   #       #',
    '# # ### # ######### #',
    '#   #   #   #       #',
    '# ### ### ### #######',
    '#   #     #         #',
    '########### #########',
    '#             #     #',
    '# ########### # ### #',
    '#     #   #   #   # #',
    '####### # # ####### #',
    '#     # #   #     # #',
    '# ### # ### # ### # #',
    '# # #   #   # # # # #',
    '# # ##### ### # # # #',
    '#   #         # # # #',
    '# ########### # # # #',
    '#       # #   # #   #',
    '####### # # ### # ###',
    '#     #   #   #   # #',
    '# # # ####### ##### #',
    '# # # #     #       #',
    '# # ### ####### #####',
    '# #       #   #     #',
    '# ### # ### # # ### #',
    '# #   # #   # #   # #',
    '### ### # ### ### # #',
    '#   #   # # #     # #',
    '# ### # # # ####### #',
    '# #   # # #   #     #',
    '# # ### # # # # ### #',
    '# # #   # # # # #   #',
    '# # # ##### ### # ###',
    '# # #     #     #   #',
    '# # ### # ######### #',
    '# #   # # #         #',
    '# ##### ### #########',
    '#   #     #   #     #',
    '##### ### ### # ### #',
    '#   # #         #   #',
    '# # # # ##### ### # #',
    '# # # # #   # #   # #',
    '# # ### # # # # ### #',
    '# #   # # # # #   # #',
    '##### # # ### ### # #',
    '#   #   #     #   # #',
    '# # ########### ### #',
    '# #   #   #   # #   #',
    '# ### # # # # # # ###',
    '# #   # # # # # #   #',
    '# # ### # ### # ### #',
    '# # #   #   # # # # #',
    '### # # ### # # # # #',
    '#   # #   #   # # # #',
    '# # # ### ##### # # #',
    '# # # # # #   #   # #',
    '# ### # # # # ##### #',
    '#   # # # # #     # #',
    '# # # # # # ##### # #',
    '# # #   # # #       #',
    '# # ##### ### #######',
    '# # #     #   #     #',
    '### # ##### ### ### #',
    '#   #       #   #   #',
    '# ######### # ##### #',
    '#     #     #     # #',
    '# ### # ######### # #',
    '# # #     #     # # #',
    '# # ### ### ### # # #',
    '# #     #   #   # # #',
    '# ##### # ### ### ###',
    '#     # # # #       #',
    '##### # # # ####### #',
    '#   # # # #   #     #',
    '# # # ### ### # ### #',
    '# # #       # #   # #',
    '# # # ##### # ##### #',
    '# #   # #   #       #',
    '# ### # # ### #######',
    '#   #   #   # #     #',
    '############# # ### #',
    '#       #     # # # #',
    '# ##### # ##### # # #',
    '#   # # # #     # # #',
    '### # # # # ##### # #',
    '#     #   # #   # # #',
    '# ######### ### # # #',
    '# #   #     #   #   #',
    '# # # # # ### # #####',
    '# # # # # #   #     #',
    '# ### ### # ####### #',
    '#         #       # #',
    '##### ######### # ###',
    '#     #       # #   #',
    '# ##### ##### ##### #',
    '#       #   #     # #',
    '# ####### # ##### # #',
    '# #       #     #   #',
    '# # ########### #####',
    '# # #   #   #   #   #',
    '# # # # # ### # # # #',
    '# # # #       #   # #',
    '# # # ######### #####',
    '# # # #   #         #',
    '# # # # # ######### #',
    '#   #   #   #     # #',
    '########### # ##### #',
    '#       #   #       #',
    '# ##### # ### # #####',
    '#   #   #   # #     #',
    '# # ####### ####### #',
    '# #       #   # #   #',
    '# ####### ### # # ###',
    '#       #   # # #   #',
    '# # ### ### # # # # #',
    '# # #   # # # #   # #',
    '# # # ### # # #######',
    '# # # #   # # #     #',
    '# # # # # # # # ### #',
    '# # #   # # # #   # #',
    '### ####### # ### # #',
    '#   #     #     # # #',
    '# ##### # # # ### # #',
    '#   #   #   #     # #',
    '##### ####### ##### #',
    '#   #   #     #     #',
    '# # ### # # #########',
    '# #   # # #   #     #',
    '# # # # # ### # # ###',
    '# # #   # #     #   #',
    '### ##### ####### # #',
    '#   #   #   # #   # #',
    '# ##### # # # # ### #',
    '#       # #   # #   #',
    '# ########### # #####',
    '# #         # # #   #',
    '### ####### # # # # #',
    '#   #       # #   # #',
    '# ##### # ### ##### #',
    '# #   # #   # #     # ',
    '# # # # ##### # #####',
    '#   # #       #    <#',
    '#####################',
]



print(Back.RED + '''==============================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
===================================================================+===============================================
==================================================================================================================
==================================================================================================================''')


tic = time.perf_counter()
escape(maze1)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
