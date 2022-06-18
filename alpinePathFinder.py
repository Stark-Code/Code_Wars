import math
import time

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

# blockPrint()


class priorityQueue:  # Min Heap
    def __init__(self):
        self.queue = []

    def enqueue(self, node, priority):
        self.queue.append({"node": node, "priority": priority})
        print(f"Node Added to Priority Queue: {node}, priority: {priority}")
        self.upHeap()

    def dequeue(self):  # Remove first element, replace with last element. downHeap as needed
        if len(self.queue) > 0:
            first = self.queue[0].copy()
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
            if self.queue[parentIdx]["priority"] > self.queue[childInd]["priority"]:
                self.queue[childInd], self.queue[parentIdx] = self.queue[parentIdx], self.queue[childInd]
                childInd = parentIdx
            else:
                break

    def downHeap(self):  # Add to top of list, compare to child. Swap as needed
        parentIdx = 0
        listLen = len(self.queue) - 1
        while True:
            swap = False
            leftChildIdx, leftChild = 2 * parentIdx + 1, float('inf')
            rightChildIdx, rightChild = 2 * parentIdx + 2, float('inf')
            if leftChildIdx <= listLen:
                leftChild = self.queue[leftChildIdx]["priority"]
                swap = True
            if rightChildIdx <= listLen:
                rightChild = self.queue[rightChildIdx]["priority"]
            if swap:
                if leftChild <= rightChild:
                    minChildIdx = leftChildIdx
                else:
                    minChildIdx = rightChildIdx
            else:
                break
            if self.queue[parentIdx]["priority"] > self.queue[minChildIdx]["priority"]:
                self.queue[minChildIdx], self.queue[parentIdx] = self.queue[parentIdx], self.queue[minChildIdx]
                parentIdx = minChildIdx
            else:
                break

    def printQueue(self):
        for x in self.queue:
            print(x)

    def getLen(self):
        return len(self.queue)


class WeightedGraph:
    def __init__(self):
        self.adjacencyList = {}

    def printGraph(self):
        for row in self.adjacencyList:
            print(f"{row} : {self.adjacencyList[row]}")

    def getWeight(self, key, neighbor):
        for x in self.adjacencyList[key]:
            if x['adjV'] == neighbor:
                return x['w']

    def printVal(self, key):
        return self.adjacencyList[key]

    def getNeighbors(self, key):
        neighbors = []
        for node in self.adjacencyList[key]:
            neighbors.append(node)
        return neighbors

    def addVertex(self, vertex):
        if vertex not in self.adjacencyList:
            self.adjacencyList.update({vertex: []})

    def addEdge(self, vertex1, vertex2, weight):
        self.adjacencyList[vertex1].append({"adjV": vertex2, "w": weight})


def initialize():
    global alpineGraph, q, distanceDict, prevNode, visited
    alpineGraph = WeightedGraph()
    q = priorityQueue()
    distanceDict = {}
    prevNode = {}
    visited = {}


def buildMaze(maze):
    return maze.splitlines()


def encode(elem1, elem2):
    return str(elem1) + "-" + str(elem2)


def searchAdj(currNode, maze):  # [y, x]

    vertex1 = encode(currNode[0], currNode[1])
    alpineGraph.addVertex(vertex1)
    searchList = []
    left, right = [currNode[0], currNode[1] - 1], [currNode[0], currNode[1] + 1]
    up, down = [currNode[0] - 1, currNode[1]], [currNode[0] + 1, currNode[1]]
    searchList.extend((left, right, up, down))
    for x in searchList:
        if 0 <= x[0] < len(maze) and 0 <= x[1] < len(maze[0]):
            vertex2 = encode(x[0], x[1])
            weight = abs(int(maze[currNode[0]][currNode[1]]) - int(maze[x[0]][x[1]]))
            alpineGraph.addEdge(vertex1, vertex2, weight)


def dijkstras(end, maze):  # alpineGraph, q, distanceDict, prevNode, visited
    while q:
        searchNode = q.dequeue()
        searchNodeXY = searchNode['node'].split('-')
        y1, x1 = int(searchNodeXY[0]), int(searchNodeXY[1])
        searchAdj([y1, x1], maze)
        if searchNode['node'] == end:
            print(f"sN: {searchNode}, end: {end}")
            print("Path Found")
            break
        neighbors = alpineGraph.getNeighbors(searchNode['node'])

        print(f"Checking Neighbors of {searchNode['node']} : {neighbors}")
        visited[searchNode['node']] = True
        print(f"Adding node {searchNode['node']} to visited list")
        for neighbor in neighbors:
            print(f"Checking Neighbor: {neighbor}")
            print(f"Checking edge weight from {neighbor['adjV']} to {searchNode['node']}")
            startWeight = alpineGraph.getWeight(searchNode['node'], neighbor['adjV'])
            print(f"Edge weight is {startWeight}")
            print(f"Home Nodes distance to A: {distanceDict[searchNode['node']]}")
            distanceWeight = startWeight + distanceDict[searchNode['node']]
            if distanceWeight < distanceDict[neighbor['adjV']]:  # neighbor['w']
                print("Updating distance dictionary")
                distanceDict[neighbor['adjV']] = distanceWeight
                print(distanceDict)
                print(f"Updated Value: {neighbor['adjV']} : {distanceDict[neighbor['adjV']]}")
                if neighbor['adjV'] not in visited:
                    q.enqueue(neighbor['adjV'], distanceDict[neighbor['adjV']])
                prevNode.update({neighbor['adjV']: searchNode['node']})
                # print(f"prevNode List: {prevNode}")
    print(f"prevNode: {prevNode}")
    return prevNode

global alpineGraph, q, distanceDict, prevNode, visited
def path_finder(maze):
    maze = buildMaze(maze)
    start = '0-0'
    initialize()

    for a in range(len(maze)):
        for z in range(len(maze[a])):
            name = encode(a, z)
            distanceDict[name] = float('inf')
            prevNode[name] = None

    # print("Weight Graph")
    # alpineGraph.printGraph()
    q.enqueue('0-0', 0)
    distanceDict['0-0'] = 0
    # print("Distance Dictionary")
    # print(distanceDict)
    prevNode['0-0'] = '0-0'
    # print("Previous Node")
    # print(prevNode)
    end = str(len(maze) - 1) + "-" + str(len(maze[-1]) - 1)
    # end = '2-3'
    # print(f"End: {end}")
    path = dijkstras(end, maze)
    print("Distance Dictionary Post Djikstra")
    print(distanceDict)
    print(f"Result: {distanceDict[end]}")
    # return distanceDict[end]
    nextNode = end
    pathToEnd = [end]
    totalWeight = 0
    while start != nextNode:
        print(f"start: {start}, nextNode: {nextNode}")
        weight = alpineGraph.getWeight(nextNode, path[nextNode])
        totalWeight += weight
        nextNode = path[nextNode]
        pathToEnd.append(nextNode)
    print(f"Total Distance: {totalWeight}")
    pathToEnd.reverse()
    print(f"Directions: {pathToEnd}")
    # return totalWeight


custom = "\n".join([  # 2,4 - 1,4 - 0,4 - 0,3 - 0,2 - 1,2 - 2,2 - 2,1 - 2,0 - 1,0 - 0,0
    "01110",
    "01110",
    "00110"
])

b = "\n".join([
    "010",
    "010",
    "010"
])

c = "\n".join([
    "91",
    "92"
])

d = "\n".join([
    "0707",
    "7070",
    "0707",
    "7070"
])

e = "\n".join([
    "700000",
    "077770",
    "077770",
    "077770",
    "077770",
    "000007"
])

f = "\n".join([
    "777000",
    "007000",
    "007000",
    "007000",
    "007000",
    "007777"
])

g = "\n".join([
    "000000",
    "000000",
    "000000",
    "000010",
    "000109",
    "001010"
])

x = [['5', '1', '8', '1', '7', '7', '6', '0', '1', '9', '7', '0', '6', '2', '2', '5', '3', '6', '0', '1', '8', '9'],
     ['7', '5', '0', '4', '1', '1', '0', '9', '0', '0', '9', '7', '8', '2', '5', '4', '4', '4', '0', '4', '7', '6'],
     ['9', '0', '1', '6', '4', '1', '9', '3', '8', '8', '4', '8', '5', '2', '1', '2', '5', '6', '8', '0', '7', '7'],
     ['8', '9', '8', '8', '0', '3', '1', '7', '5', '7', '6', '4', '3', '8', '9', '7', '8', '0', '6', '5', '7', '2'],
     ['4', '3', '9', '4', '4', '4', '7', '1', '3', '6', '5', '7', '3', '5', '2', '2', '8', '2', '9', '7', '0', '8'],
     ['6', '9', '5', '9', '8', '8', '5', '3', '1', '4', '2', '4', '4', '2', '0', '1', '0', '5', '0', '4', '9', '5'],
     ['2', '7', '7', '8', '0', '7', '8', '0', '3', '8', '7', '4', '6', '6', '4', '6', '1', '2', '9', '0', '2', '3'],
     ['3', '1', '4', '7', '7', '1', '1', '9', '9', '1', '7', '1', '7', '4', '8', '1', '5', '7', '5', '6', '6', '3'],
     ['6', '8', '5', '5', '8', '3', '8', '0', '1', '2', '6', '6', '2', '9', '6', '8', '7', '5', '9', '6', '6', '2'],
     ['2', '5', '7', '2', '2', '5', '3', '2', '5', '0', '0', '3', '0', '6', '9', '8', '0', '2', '6', '3', '7', '4'],
     ['9', '9', '2', '3', '5', '6', '0', '3', '2', '1', '6', '7', '0', '9', '5', '4', '8', '9', '2', '4', '0', '5'],
     ['4', '2', '2', '6', '8', '2', '9', '3', '5', '3', '1', '1', '8', '2', '1', '1', '3', '5', '6', '0', '4', '0'],
     ['0', '9', '0', '0', '8', '6', '3', '8', '2', '9', '5', '9', '5', '9', '6', '7', '3', '5', '1', '8', '4', '2'],
     ['6', '5', '4', '9', '1', '8', '4', '4', '0', '0', '8', '1', '0', '1', '7', '2', '0', '5', '4', '3', '1', '9'],
     ['3', '5', '5', '0', '2', '0', '3', '1', '3', '4', '0', '8', '2', '5', '9', '1', '9', '6', '6', '4', '4', '4'],
     ['0', '6', '2', '3', '2', '4', '0', '2', '6', '8', '1', '6', '6', '6', '2', '5', '5', '8', '9', '1', '8', '6'],
     ['3', '3', '3', '5', '2', '9', '8', '0', '2', '4', '7', '6', '1', '1', '3', '0', '2', '9', '8', '5', '3', '0'],
     ['9', '5', '1', '1', '4', '6', '6', '1', '5', '5', '5', '0', '5', '2', '9', '8', '7', '8', '9', '7', '2', '7'],
     ['6', '1', '2', '5', '8', '5', '2', '7', '0', '7', '6', '3', '6', '3', '6', '8', '1', '6', '1', '6', '8', '2'],
     ['1', '6', '8', '1', '2', '6', '7', '4', '4', '1', '2', '6', '1', '9', '1', '7', '6', '1', '8', '3', '2', '7'],
     ['5', '8', '7', '3', '1', '5', '4', '5', '0', '8', '8', '9', '8', '1', '5', '1', '6', '4', '1', '2', '1', '5'],
     ['2', '8', '9', '0', '7', '6', '9', '2', '7', '6', '0', '5', '6', '6', '5', '7', '0', '4', '8', '5', '5', '0']]


tic = time.perf_counter()
path_finder(g)
toc = time.perf_counter()
enablePrint()
print(f"Time: {toc - tic:0.4f} seconds")

# Initialize PriorityQueue, ShortestDistanceDictionary, VisitedList, PreviousDictionary
# 1Move through neighbors of A: start alphabeticaly perhaps
# 2compare the edge from A to neighbor with the shortestDistanceDictionary value. If it is less, then update that value
# 3Go into previous dictionary, and update neighbor value to A
# 4Move onto next adj neighbor of A
# 2
# 3
# 4 After all neighbors of A have been visited. Mark A in visited List. Find lowest value in shortedDistanceDict. Step 1

#         1   - 0
#        2 3  - 1, 2
#     4 5  6 7 -3,4 - 5, 6
#
# index 6 parent = 2
# Math.floor(6 - 1 / 2?) Math.floor((ind - 1)/2)

# Might be a problem not initializing distance dictionary with values
#
# q.enqueue("a", 8)
# q.enqueue("b", 7)
# q.enqueue("c", 2)
# q.enqueue("d", 17)
# q.enqueue("e", 4)
# q.enqueue("f", 11)
# q.enqueue("g", 1)
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()
# q.dequeue()
# q.printQueue()

#
# y = [['6', '9', '6', '5', '3', '1', '1', '5', '7', '5', '3', '8', '4', '0', '2', '1', '5', '3', '5', '0', '7', '2', '5'],
#      ['2', '5', '6', '5', '5', '9', '1', '1', '7', '7', '3', '0', '7', '3', '4', '1', '3', '1', '4', '7', '7', '1', '4'],
#      ['9', '3', '3', '4', '9', '4', '7', '4', '2', '6', '9', '1', '2', '9', '8', '6', '0', '2', '3', '4', '5', '7', '2'],
#      ['0', '1', '2', '4', '8', '5', '2', '2', '8', '8', '8', '8', '9', '3', '1', '5', '5', '4', '1', '5', '3', '4', '4'],
#      ['8', '4', '5', '8', '4', '9', '9', '7', '7', '0', '2', '6', '5', '1', '7', '7', '5', '9', '8', '6', '0', '6', '0'],
#      ['4', '3', '1', '8', '1', '4', '6', '8', '1', '8', '2', '7', '2', '5', '1', '0', '7', '6', '0', '4', '6', '2', '3'],
#      ['9', '8', '3', '9', '3', '4', '8', '1', '1', '7', '0', '3', '6', '1', '0', '4', '1', '9', '2', '4', '5', '0', '1'],
#      ['2', '0', '5', '3', '2', '2', '4', '0', '8', '2', '0', '2', '2', '5', '0', '6', '5', '8', '7', '1', '9', '7', '8'],
#      ['2', '2', '2', '3', '3', '5', '6', '7', '5', '2', '4', '9', '0', '3', '6', '8', '6', '4', '6', '6', '6', '0', '5'],
#      ['7', '0', '7', '6', '1', '1', '4', '3', '7', '8', '1', '6', '1', '4', '5', '0', '0', '9', '1', '1', '9', '3', '1'],
#      ['5', '4', '9', '5', '3', '6', '7', '1', '4', '9', '2', '2', '2', '7', '5', '7', '2', '9', '5', '7', '7', '6', '3'],
#      ['4', '5', '9', '3', '1', '0', '4', '0', '9', '5', '0', '8', '9', '3', '1', '3', '4', '1', '0', '5', '8', '7', '1'],
#      ['1', '9', '0', '1', '3', '5', '8', '8', '1', '7', '4', '5', '6', '2', '6', '9', '0', '6', '1', '5', '9', '3', '8'],
#      ['2', '7', '0', '5', '0', '0', '7', '2', '8', '2', '0', '7', '5', '5', '4', '3', '8', '6', '4', '6', '7', '8', '8'],
#      ['0', '6', '5', '2', '8', '2', '1', '3', '8', '0', '1', '2', '0', '2', '2', '0', '6', '2', '5', '2', '8', '1', '9'],
#      ['3', '8', '1', '7', '6', '2', '7', '0', '5', '0', '1', '7', '4', '5', '1', '9', '2', '1', '7', '1', '3', '6', '7'],
#      ['3', '1', '3', '0', '4', '3', '0', '7', '1', '9', '2', '1', '5', '2', '6', '1', '5', '9', '5', '2', '5', '3', '1'],
#      ['6', '8', '1', '5', '8', '7', '6', '2', '3', '6', '0', '8', '9', '2', '1', '8', '0', '4', '6', '1', '6', '6', '5'],
#      ['0', '9', '8', '2', '7', '8', '4', '0', '9', '7', '3', '1', '2', '0', '4', '0', '1', '9', '9', '7', '4', '9', '8'],
#      ['9', '7', '5', '1', '8', '9', '8', '0', '5', '3', '4', '1', '6', '0', '4', '2', '6', '8', '7', '2', '8', '1', '1'],
#      ['1', '2', '1', '8', '5', '1', '4', '2', '9', '8', '2', '8', '8', '7', '0', '4', '9', '3', '1', '2', '8', '1', '7'],
#      ['8', '6', '0', '8', '8', '5', '1', '1', '1', '4', '5', '4', '4', '1', '8', '1', '9', '2', '6', '1', '2', '1', '8'],
#      ['2', '9', '4', '5', '3', '5', '8', '4', '1', '7', '7', '4', '0', '2', '0', '2', '9', '7', '6', '0', '3', '9', '7']]

