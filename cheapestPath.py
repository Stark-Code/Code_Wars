import sys
import border
import math
import time
import copy


class priorityQueue:  # Min Heap
    def __init__(self):
        self.queue = []

    def enqueue(self, node):
        self.queue.append(node)
        print(f"Node Added to Priority Queue: {node.__str__()}")
        self.upHeap()

    def dequeue(self):  # Remove first element, replace with last element. downHeap as needed
        if len(self.queue) > 0:
            first = copy.deepcopy(self.queue[0])
            lastElement = self.queue.pop(-1)
            if len(self.queue) > 0:
                self.queue[0] = lastElement
                self.downHeap()
                return first
            else:
                return lastElement

    def upHeap(self):  # Enqueue (Add to end of list. Compare it to parent, swap as needed
        childInd = len(self.queue) - 1
        while childInd > 0:
            parentIdx = math.floor((childInd - 1) / 2)
            if self.queue[parentIdx].fCost > self.queue[childInd].fCost:
                self.queue[childInd], self.queue[parentIdx] = self.queue[parentIdx], self.queue[childInd]
                childInd = parentIdx
            else:
                break

    def downHeap(self):  # Add to top of list, compare to child. Swap as needed
        parentIdx = 0
        listLen = len(self.queue) - 1
        while True:
            l_Swap = False
            r_Swap = False
            leftChildIdx, leftChild = 2 * parentIdx + 1, float('inf')
            rightChildIdx, rightChild = 2 * parentIdx + 2, float('inf')
            if leftChildIdx <= listLen:
                leftChild = self.queue[leftChildIdx]
                l_Swap = True
            if rightChildIdx <= listLen:
                rightChild = self.queue[rightChildIdx]
                r_Swap = True
            if l_Swap and r_Swap:
                if leftChild.fCost <= rightChild.fCost:
                    minChildIdx = leftChildIdx
                else:
                    minChildIdx = rightChildIdx
            elif l_Swap: minChildIdx = leftChildIdx
            else:
                break
            if self.queue[parentIdx].fCost > self.queue[minChildIdx].fCost:
                self.queue[minChildIdx], self.queue[parentIdx] = self.queue[parentIdx], self.queue[minChildIdx]
                parentIdx = minChildIdx
            else:
                break

    def printQueue(self):
        for x in self.queue:
            print(x)


class Node:
    def __init__(self, pos, w):
        self.position = pos
        self.fCost = float('Inf')
        self.closed = False
        self.weight = w
        self.parent = None

    def __str__(self):
        return self.weight


def printGrid(grid):
    for row in grid:
        temp = []
        for x in row:
            temp.append(x.__str__())
        print(temp)


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
        # neighbors = searchAdjNodes(currNode, grid)
        # for n in neighbors:
        #     q.enqueue(n)
        # currNode = q.dequeue()
        # currNode.closed = True

        minCost = float('Inf')

        for nodeIdx, node in enumerate(nodeTracker):
            if not node.closed:
                # print(f'NodeTracker: Position {node.position}, Weight: {node.weight}, fCost {node.fCost}')
                if node.fCost < minCost:
                    minCostNode = node
                    minNodeIdx = nodeIdx
                    minCost = node.fCost
        # print(f'Next Node: Position {minCostNode.position}, Weight: {minCostNode.weight}, fCost {minCostNode.fCost}')
        currNode = minCostNode
        currNode.closed = True





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
    print(f'Start: {start}, Finish: {finish}')
    # q = priorityQueue()
    for row in t:
        print(row)
    grid = [[Node((yIdx, xIdx), t[yIdx][xIdx]) for xIdx, x in enumerate(y)] for yIdx, y in enumerate(t)]
    startNode = Node(start, t[start[0]][start[1]])
    startNode.fCost, startNode.closed, startNode.parent = t[start[0]][start[1]], True, 'Origin'
    grid[start[0]][start[1]] = startNode
    bfs(startNode, finish, grid, nodeTracker=[])
    return getDirections(grid[finish[0]][finish[1]])


tic = time.perf_counter()
border.printBorder()
r = cheapest_path([[1, 9, 1], [2, 9, 1], [2, 1, 1]], (0, 0), (0, 2))
print(r)
r = cheapest_path([[1, 4, 1], [1, 9, 1], [1, 1, 1]], (0, 0), (0, 2))
print(r)
r = cheapest_path([[1, 19, 1, 1, 1],
                   [1, 19, 1, 19, 1],
                   [1, 19, 1, 19, 1],
                   [1, 19, 1, 19, 1],
                   [1, 1, 1, 19, 1]], (0, 0), (4, 4))
print(r)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
# .004 s with list
