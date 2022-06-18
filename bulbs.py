import time


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.adjList = []
        self.visited = False

def searchNeighbors(currNode, nodeIdx, nodes):  # Changed from position to object
    rF, drF, dF, dlF = False, False, False, False  # downLeft found, right found etc.

    def addNeighbors(_node, neighbor):
        _node.adjList.append(neighbor)
        neighbor.adjList.append(_node)

    for node in range(nodeIdx + 1, len(nodes)):
        if currNode.pos[0] == nodes[node].pos[0] and not dF:
            addNeighbors(currNode, nodes[node]); dF = True
        if currNode.pos[1] == nodes[node].pos[1] and not rF:
            addNeighbors(currNode, nodes[node]); rF = True
        if abs(currNode.pos[0] - nodes[node].pos[0]) == abs(currNode.pos[1] - nodes[node].pos[1]):
            if currNode.pos[1] < nodes[node].pos[1] and not drF:
                addNeighbors(currNode, nodes[node]); drF = True
            elif currNode.pos[1] > nodes[node].pos[1] and not dlF:
                addNeighbors(currNode, nodes[node]); dlF = True


def dfs(currNode, route, total):
    if len(route) == total:
        return True, route
    currNode.visited = True
    for neighbor in currNode.adjList:
        if not neighbor.visited:
            route.append(neighbor.pos)
            solutionFound, route = dfs(neighbor, route, total)
            if solutionFound:
                return True, route
    currNode.visited = False
    route.pop()
    return False, route


def switch_bulbs(game_map):
    nodes = []
    for yIdx, y in enumerate(game_map.split('\n')):
        for xIdx, x in enumerate(list(y)):
            if x == 'B':
                node = Node((yIdx - 1, xIdx - 1))
                nodes.append(node)
    for nodeIdx in range(len(nodes) - 1):
        searchNeighbors(nodes[nodeIdx], nodeIdx, nodes)
    for node in nodes:  # Driver
        solutionFound, route = dfs(node, route=[node.pos], total=len(nodes))
        if solutionFound: break
    else: return None
    return route


examples = [
    [(5, 3), (1, 3)],
    [(1, 3), (3, 5), (5, 3)],
    [(1, 3), (5, 3), (7, 5)],
    [(1, 3), (5, 3), (7, 5), (7, 1), (2, 1)],
    [(1, 3), (5, 3), (7, 5), (7, 1), (2, 1), (5, 4)],
]

GAME_MAPS = [
    "+--------+\n" +
    "|....B..B|\n" +
    "|........|\n" +
    "|........|\n" +
    "|........|\n" +
    "|........|\n" +
    "|........|\n" +
    "|....B...|\n" +
    "|........|\n" +
    "+--------+",

    "+--------+\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|.....B..|\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|........|\n" +
    "+--------+",

    "+--------+\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|........|\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|.....B..|\n" +
    "+--------+",

    "+--------+\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|.B......|\n" +
    "|........|\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|.B...B..|\n" +
    "+--------+",

    "+--------+\n" +
    "|........|\n" +
    "|...B....|\n" +
    "|.B......|\n" +
    "|........|\n" +
    "|........|\n" +
    "|...BB...|\n" +
    "|........|\n" +
    "|.B...B..|\n" +
    "+--------+",

    "+--------+\n" +
    "|...B....|\n" +
    "|........|\n" +
    "|.B......|\n" +
    "|......B.|\n" +
    "|......B.|\n" +
    "|.B......|\n" +
    "|......BB|\n" +
    "|BB......|\n" +
    "+--------+",
]

tic = time.perf_counter()
switch_bulbs(GAME_MAPS[5])
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

'''
Driver function searching through all nodes for path
Start with node, mark as visited
Loop through adj list, if no more nodes to visit and no solution, mark node unvisited, recurse to prev node. Check next 
'''
