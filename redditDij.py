import math


class priorityQueue:  # Min Heap
    def __init__(self):
        self.queue = []

    def enqueue(self, node, priority):
        self.queue.append({"node": node, "priority": priority})
        print(f"Node Added to Priority Queue: {node}, priority: {priority}")
        self.upHeap()

    def dequeue(self):
        if len(self.queue) > 0:
            first = self.queue[0].copy()
            lastElement = self.queue.pop(-1)
            if len(self.queue) > 0:
                self.queue[0] = lastElement
                self.downHeap()
                return first
            else:
                return lastElement

    def upHeap(self):
        childInd = len(self.queue) - 1
        while childInd > 0:
            parentIdx = math.floor((childInd - 1) / 2)
            if self.queue[parentIdx]["priority"] > self.queue[childInd]["priority"]:
                self.queue[childInd], self.queue[parentIdx] = self.queue[parentIdx], self.queue[childInd]
                childInd = parentIdx
            else:
                break

    def downHeap(self):
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

class WeightedGraph:
    def __init__(self):
        self.adjacencyList = {}

    def getWeight(self, key, neighbor):
        for x in self.adjacencyList[key]:
            if x['adjV'] == neighbor:
                return x['w']

    def getNeighbors(self, key):
        neighbors = []
        for node in self.adjacencyList[key]:
            neighbors.append(node)
        return neighbors

    def addVertex(self, vertex):
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
            break
        neighbors = alpineGraph.getNeighbors(searchNode['node'])
        visited[searchNode['node']] = True
        for neighbor in neighbors:
            startWeight = alpineGraph.getWeight(searchNode['node'], neighbor['adjV'])
            distanceWeight = startWeight + distanceDict[searchNode['node']]
            if distanceWeight < distanceDict[neighbor['adjV']]:
                distanceDict[neighbor['adjV']] = distanceWeight
                if neighbor['adjV'] not in visited:
                    q.enqueue(neighbor['adjV'], distanceDict[neighbor['adjV']])
                prevNode.update({neighbor['adjV']: searchNode['node']})
    return prevNode


def path_finder(maze):
    maze = maze.splitlines()
    initialize()

    for a in range(len(maze)):
        for z in range(len(maze[a])):
            name = encode(a, z)
            distanceDict[name] = float('inf')
            prevNode[name] = None
    q.enqueue('0-0', 0)
    distanceDict['0-0'] = 0
    prevNode['0-0'] = '0-0'
    end = str(len(maze) - 1) + "-" + str(len(maze[-1]) - 1)
    dijkstras(end, maze)
    return distanceDict[end]

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
path_finder(x)
toc = time.perf_counter()
enablePrint()
print(f"Time: {toc - tic:0.4f} seconds")
