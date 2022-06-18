class Node:
    def __init__(self, pos, w):
        self.position = pos
        self.fCost = float('Inf')
        self.closed = False
        self.weight = w
        self.parent = None


def searchAdjNodes(parentNode, grid):
    nodeTracker = []
    for searchPos in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        searchSquare = [parentNode.position[0] + searchPos[0], parentNode.position[1] + searchPos[1]]
        if 0 <= searchSquare[0] < len(grid) and 0 <= searchSquare[1] < len(grid[0]):
            childNode = grid[searchSquare[0]][searchSquare[1]]
            if not childNode.closed:
                currPath_F_Cost = parentNode.fCost + childNode.weight
                if childNode.fCost == float('Inf'):
                    nodeTracker.append(childNode)
                if currPath_F_Cost < childNode.fCost:
                    childNode.fCost = currPath_F_Cost
                    childNode.parent = parentNode
    return nodeTracker


def bfs(currNode, finish, grid, nodeTracker):
    while currNode.position != finish:
        nodeTracker.extend(searchAdjNodes(currNode, grid))
        minCost = float('Inf')

        for nodeIdx, node in enumerate(nodeTracker):
            if not node.closed:
                if node.fCost < minCost:
                    minCostNode = node
                    minNodeIdx = nodeIdx
                    minCost = node.fCost
        currNode = minCostNode
        currNode.closed = True
        nodeTracker[-1], nodeTracker[minNodeIdx] = nodeTracker[minNodeIdx], nodeTracker[-1]
        nodeTracker.pop(-1)


def getDirections(node):  # Start from finish node
    directions = []
    while node.parent != 'Origin':  # All direction reversed since Im coming from finish
        if node.position[0] > node.parent.position[0]: directions.append('down')
        elif node.position[0] < node.parent.position[0]: directions.append('up')
        elif node.position[1] > node.parent.position[1]: directions.append('right')
        elif node.position[1] < node.parent.position[1]: directions.append('left')
        node = node.parent
    directions.reverse()
    return directions


def cheapest_path(t, start, finish):
    grid = [[Node((yIdx, xIdx), t[yIdx][xIdx]) for xIdx, x in enumerate(y)] for yIdx, y in enumerate(t)]
    startNode = Node(start, t[start[0]][start[1]])
    startNode.fCost, startNode.closed, startNode.parent = t[start[0]][start[1]], True, 'Origin'
    grid[start[0]][start[1]] = startNode
    bfs(startNode, finish, grid, nodeTracker=[])
    return getDirections(grid[finish[0]][finish[1]])
