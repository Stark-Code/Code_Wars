import copy
import time

_dotMatrix = {
    'A': ['B', 'D', 'E', 'F', 'H'],
    'B': ['A', 'C', 'D', 'E', 'F', 'G', 'I'],
    'C': ['B', 'D', 'E', 'F', 'H'],
    'D': ['A', 'B', 'C', 'E', 'G', 'H', 'I'],
    'E': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I'],
    'F': ['A', 'B', 'C', 'E', 'G', 'H', 'I'],
    'G': ['B', 'D', 'E', 'F', 'H'],
    'H': ['A', 'C', 'D', 'E', 'F', 'G', 'I'],
    'I': ['B', 'D', 'E', 'F', 'H']
}

discoveredNodes = {
    'B': [['A', 'C'], ['C', 'A']],
    'D': [['A', 'G'], ['G', 'A']],
    'E': [['A', 'I'], ['B', 'H'], ['C', 'G'], ['D', 'F'], ['F', 'D'], ['G', 'C'], ['H', 'B'], ['I', 'A']],
    'F': [['C', 'I'], ['I', 'C']],
    'H': [['G', 'I'], ['I', 'G']]
}

learnedPatterCounts = {
    'corner': {},
    'center': {},
    'cross': {}
}


def recursiveDFS(visitedNodes, dotMatrix, length, count):
    if len(visitedNodes) == length:
        count += 1
        return count

    dotMatrixClone = copy.deepcopy(dotMatrix)
    if visitedNodes[-1] in discoveredNodes:
        for discoveredNode in discoveredNodes[visitedNodes[-1]]:
            dotMatrixClone[discoveredNode[0]].extend(discoveredNode[1])

    for node in dotMatrixClone[visitedNodes[-1]]:
        if node not in visitedNodes:
            visitedNodesClone = copy.deepcopy(visitedNodes)
            visitedNodesClone.append(node)
            count = recursiveDFS(visitedNodesClone, dotMatrixClone, length, count)
    return count


def checkLearnedPatterns(firstPoint, length):
    if firstPoint in ['A', 'C', 'G', 'I']:
        if length in learnedPatterCounts['corner']:
            return learnedPatterCounts['corner'][length]
    elif firstPoint in ['B', 'D', 'F', 'H']:
        if length in learnedPatterCounts['cross']:
            return learnedPatterCounts['cross'][length]
    elif firstPoint == 'E':
        if length in learnedPatterCounts['center']:
            return learnedPatterCounts['center'][length]
    return False


def addFoundPattern(firstPoint, length, count):
    if firstPoint in ['A', 'C', 'G', 'I']:
        learnedPatterCounts['corner'][length] = count
    elif firstPoint in ['B', 'D', 'F', 'H']:
        learnedPatterCounts['cross'][length] = count
    elif firstPoint == 'E':
        learnedPatterCounts['center'][length] = count


def count_patterns_from(firstPoint, length):
    existingResult = checkLearnedPatterns(firstPoint, length)  # Check memoization
    if existingResult: return existingResult

    if length < 1 or length > 9: return 0
    visited = [firstPoint]
    count = recursiveDFS(visited, _dotMatrix, length, count=0)
    addFoundPattern(firstPoint, length, count)
    return count


tic = time.perf_counter()
r = count_patterns_from('C', 2)
count_patterns_from('A', 6)
count_patterns_from('A', 7)
count_patterns_from('A', 8)
count_patterns_from('A', 3)
count_patterns_from('C', 6)
count_patterns_from('A', 6)
count_patterns_from('D', 7)
count_patterns_from('F', 8)
count_patterns_from('G', 3)
count_patterns_from('E', 6)
count_patterns_from('I', 6)
count_patterns_from('C', 7)
count_patterns_from('B', 8)
count_patterns_from('A', 3)
count_patterns_from('C', 6)

toc = time.perf_counter()
print(f'Count: {r}')
print(f"Time: {toc - tic:0.4f} seconds")





#
# import copy
# import time
# count = 0
# _dotMatrix = {
#     'A': ['B', 'D', 'E', 'F', 'H'],
#     'B': ['A', 'C', 'D', 'E', 'F', 'G', 'I'],
#     'C': ['B', 'D', 'E', 'F', 'H'],
#     'D': ['A', 'B', 'C', 'E', 'G', 'H', 'I'],
#     'E': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I'],
#     'F': ['A', 'B', 'C', 'E', 'G', 'H', 'I'],
#     'G': ['B', 'D', 'E', 'F', 'H'],
#     'H': ['A', 'C', 'D', 'E', 'F', 'G', 'I'],
#     'I': ['B', 'D', 'E', 'F', 'H']
# }
#
# discoveredNodes = {
#     'B': [['A', 'C'], ['C', 'A']],
#     'D': [['A', 'G'], ['G', 'A']],
#     'E': [['A', 'I'], ['B', 'H'], ['C', 'G'], ['D', 'F'], ['F', 'D'], ['G', 'C'], ['H', 'B'], ['I', 'A']],
#     'F': [['C', 'I'], ['I', 'C']],
#     'H': [['G', 'I'], ['I', 'G']]
# }
#
#
# def recursiveDFS(visitedNodes, dotMatrix, length):
#     print(length)
#     if len(visitedNodes) == length:
# #         print(visitedNodes)
#         global count
#         count += 1
#         return
#     dotMatrixClone = copy.deepcopy(dotMatrix)
#     if visitedNodes[-1] in discoveredNodes:
#         for discoveredNode in discoveredNodes[visitedNodes[-1]]:
#             # print(discoveredNode)
#             # print(dotMatrixClone)
#             dotMatrixClone[discoveredNode[0]].extend(discoveredNode[1])
#     for node in dotMatrix[visitedNodes[-1]]:
#         if node not in visitedNodes:
#             visitedNodesClone = copy.deepcopy(visitedNodes)
#             visitedNodesClone.append(node)
#             recursiveDFS(visitedNodesClone, dotMatrixClone, length)
#
#
# def count_patterns_from(firstPoint, length):
#     if length < 1 or length > 9: return 0
#     global count
#     count = 0
#     visited = [firstPoint]
#     recursiveDFS(visited, _dotMatrix, length)
#     return count
