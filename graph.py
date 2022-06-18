class Graph:
    def __init__(self):
        self.adjacenyList = {}

    def addNode(self, vertex):
        if vertex in self.adjacenyList:
            print('Node already exists!')
        else: self.adjacenyList[vertex] = []

    def addEdge(self, vertex1, vertex2):
        if vertex1 in self.adjacenyList:
            self.adjacenyList[vertex1].append(vertex2)
        else:
            self.adjacenyList[vertex1] = [vertex2]
        if vertex2 in self.adjacenyList:
            self.adjacenyList[vertex2].append(vertex1)
        else:
            self.adjacenyList[vertex2] = [vertex1]

    def removeEdge(self, vertex1, vertex2):
        self.adjacenyList[vertex1] = list(filter(lambda x: x != vertex2, self.adjacenyList[vertex1]))
        self.adjacenyList[vertex2] = list(filter(lambda x: x != vertex1, self.adjacenyList[vertex2]))

    def removeVertex(self, vertex):
        for v in self.adjacenyList:
            self.removeEdge(vertex, v)
        del self.adjacenyList[vertex]

    def printGraph(self):
        for key, value in self.adjacenyList.items():
            print(f'{key}: {value}')

g = Graph()
g.addEdge("A", "B")
g.addEdge("A", "C")
g.printGraph()
# g.removeEdge("A", "B")
g.removeVertex("B")
g.printGraph()