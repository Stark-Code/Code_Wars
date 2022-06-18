import copy
import math
import border


class Node:
    def __init__(self, location):
        self.location = location
        self.gCost = float('Inf')
        self.hCost = float('Inf')
        self.fCost = float('Inf')
        self.closed = False
        self.parent = None

    def __str__(self):
        if self.fCost == float('inf'):
            return '0'
        else:
            return str(self.fCost)


def printGrid(grid):
    for row in grid:
        temp = []
        for x in row:
            if isinstance(x, Node):
                temp.append(x.__str__())
            else:
                temp.append(x)
        print(temp)
    print('')


def find_Start_and_End(grid):
    start = end = None
    for rowIdx, row in enumerate(grid):
        for colIdx, col in enumerate(row):
            if col == 'S': start = [rowIdx, colIdx]
            elif col == 'G': end = [rowIdx, colIdx]
    return start, end


def getDirections(grid, end, start, solution):
    node = grid[end[0]][end[1]]
    while node.parent != 'Home':
        node = copy.copy(node.parent)
        solution[node.location[0]][node.location[1]] = 'P'
    solution[start[0]][start[1]] = 'S'
    return '\n'.join(''.join(item) for item in solution)


def getPriorityNode(nodeTracker):
    min_F_Cost, minNode = float('Inf'), None
    for nodeIdx, node in enumerate(nodeTracker):  # Prioritize next node
        if node.fCost < min_F_Cost and not node.closed:
            minNode = node
            minNodeIdx = nodeIdx
            min_F_Cost = node.fCost
    if minNode is None:
        return "Oh for crying out loud...", None
    currNode = minNode
    currNode.closed = True
    nodeTracker.pop(minNodeIdx)
    return nodeTracker, currNode


def exploreNeighbors(grid, end, currNode, nodeTracker):
    for searchPos in [[-1, 0, 'C'], [-1, 1, 'D'], [0, 1, 'C'], [1, 1, 'D'], [1, 0, 'C'], [1, -1, 'D'],
                      [0, -1, 'C'], [-1, -1, 'D']]:
        searchSquare = [currNode.location[0] + searchPos[0], currNode.location[1] + searchPos[1]]
        if 0 <= searchSquare[0] < len(grid) and 0 <= searchSquare[1] < len(grid[0]):
            if isinstance(grid[searchSquare[0]][searchSquare[1]], Node):
                foundNode = grid[searchSquare[0]][searchSquare[1]]
                if not foundNode.closed:
                    nodeTracker.append(foundNode)
                dy_End = abs(searchSquare[0] - end[0])
                dx_End = abs(searchSquare[1] - end[1])
                if searchPos[2] == "D":
                    path_G_Cost = currNode.gCost + 1.4
                else:
                    path_G_Cost = currNode.gCost + 1
                path_H_Cost = round(math.sqrt(dy_End ** 2 + dx_End ** 2), 2)
                path_F_Cost = path_H_Cost + path_G_Cost
                if path_G_Cost < foundNode.gCost:
                    foundNode.hCost = path_H_Cost
                    foundNode.gCost = path_G_Cost
                    foundNode.fCost = path_F_Cost
                    foundNode.parent = currNode
                if foundNode.location == end:
                    return True


def BFS(grid, currNode, start, end, solution):
    nodeTracker = []
    solutionFound = False
    while not solutionFound:
        solutionFound = exploreNeighbors(grid, end, currNode, nodeTracker)

        if len(nodeTracker) == 0 or solutionFound: break
        nodeTracker, currNode = getPriorityNode(nodeTracker)
        if currNode is None:
            return "Oh for crying out loud..."
    if solutionFound:
        return getDirections(grid, end, start, solution)
    else:
        return "Oh for crying out loud..."


def wire_DHD_SG1(existing_wires):
    print(existing_wires)
    grid = [[Node([yIdx, xIdx]) if x == '.' else x for xIdx, x in enumerate(y)] for yIdx, y in enumerate(existing_wires.split('\n'))]
    solution = [[x for x in y] for y in existing_wires.split('\n')]
    start, end = find_Start_and_End(grid)
    startNode, endNode = Node(start), Node(end)
    startNode.fCost, startNode.gCost, startNode.hCost, startNode.closed, startNode.parent = 0, 0, 0, True, 'Home'
    endNode.parent = 'End'
    grid[end[0]][end[1]] = endNode
    return BFS(grid, startNode, start, end, solution)


# Maze format may cause problems
maze = '''.S...
XXX..
.X.XX
..X..
G...X'''

maze1 = '''X..XX...
X.XXXX.X
X....XXX
.XXXS.XX
XX....X.
..XX...X
XX...X.X
XX.G...X'''

border.printBorder()
r = wire_DHD_SG1(maze1)
print(r)