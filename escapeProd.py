import copy
import time
from colorama import init, Back

init(autoreset=True)


class Player:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.visited = [position]  # Nodes visited
        self.route = []  # Movements made to get to current position
        self.priorities = None  # Prioritized list of nodes in respect to Manhattan Distance
        self.storage = None

    def setVisited(self, node):
        self.visited.append(node)

    def setPosition(self, position):
        self.position = position

    def __str__(self):
        return self.orientation


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


def findPlayer(maze):
    for yIdx, y in enumerate(maze):
        for xIdx, x in enumerate(y):
            if x in ['^', 'v', '>', '<']:
                return (yIdx, xIdx), x


def findExits(maze):
    exits, lastRow, lastCol = [], len(maze) - 1, len(maze[0]) - 1
    for xIdx, x in enumerate(maze[0]):
        if x == ' ': exits.append((0, xIdx))
    for yIdx in range(1, lastRow):
        if maze[yIdx][0] == ' ': exits.append((yIdx, 0))
        if maze[yIdx][lastCol] == ' ': exits.append((yIdx, lastCol))
    for xIdx, x in enumerate(maze[lastRow]):
        if x == ' ': exits.append((lastRow, xIdx))
    return exits


def findNeighbors(player, maze, _exit):
    availableNodes = []
    routeData = []
    orientationNumeric = orientationCode[player.orientation]
    for searchPos in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        searchSquare = (player.position[0] + searchPos[0], player.position[1] + searchPos[1])
        if 0 <= searchSquare[0] < len(maze) and 0 <= searchSquare[1] < len(maze[0]):
            if maze[searchSquare[0]][searchSquare[1]] == ' ' and searchSquare not in player.visited:
                availableNodes.append(searchSquare)
                directionMod = (searchPos[0] + orientationNumeric[0], searchPos[1] + orientationNumeric[1])
                routeData.append(directionDict[player.orientation][directionMod])
    if len(availableNodes) > 0:
        availableNodes, routeData = zip(*sorted(zip(availableNodes, routeData),
                                                key=lambda node: abs(node[0][0] - _exit[0]) + abs(
                                                    node[0][1] - _exit[1])))
    else: maze[player.position[0]][player.position[1]] = '#'
    return availableNodes, routeData, maze  # routeData: Directions, Orientation


def recursiveSearch(player, maze, _exit):
    if player.position == _exit:
        return True, player.route

    player.priorities, player.storage, maze = findNeighbors(player, maze, _exit)

    for idx, nodeToVisit in enumerate(player.priorities):
        playerInstance = copy.deepcopy(player)
        playerInstance.setPosition(nodeToVisit)
        playerInstance.visited.append(nodeToVisit)
        playerInstance.orientation = playerInstance.storage[idx][1]
        playerInstance.route.extend(playerInstance.storage[idx][0])
        routeFound, route = recursiveSearch(playerInstance, maze, _exit)
        if routeFound:
            return True, route
    return False, []  # No exit found


def escape(maze):
    maze = [[x for x in y] for y in maze]
    playerPos, orientation = findPlayer(maze)
    player = Player(playerPos, orientation)
    exits = findExits(maze)
    exits.sort(key=lambda _exit: abs(player.position[0] - _exit[0]) + abs(player.position[1] - _exit[1]))
    for _exit in exits:
        routeFound, route = recursiveSearch(player, maze, _exit)
        if routeFound: break
    else:
        route = []
    print(f'Result: {route}')
    return route

maze1 = [
    '##### #####',
    '##        #',
    '#   ##### #',
    '# ### #  ##',
    '# # #^*# # #',
    '# # # # # #',
    '#       # #',
    '##### #####'
]

maze2 = ["##### ###################################",
         "#<    #       #     #         # #   #   #",
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

