import logging

logging.basicConfig(level=logging.INFO, format=' - %(message)s')
logging.disable(logging.CRITICAL)
searchParams = [[0, -1], [-1, 0], [0, 1], [-1, 0]]

pipeDict = {  # Y axis change(s) listed first
    '┗': ((-1, 0), (0, 1)),
    '┓': ((1, 0), (0, -1)),
    '┏': ((1, 0), (0, 1)),
    '┛': ((-1, 0), (0, -1)),
    '━': ((0, -1), (0, 1)),
    '┃': ((-1, 0), (1, 0)),
    '┣': ((-1, 0), (1, 0), (0, 1)),
    '┫': ((-1, 0), (1, 0), (0, -1)),
    '┳': ((1, 0), (0, -1), (0, 1)),
    '┻': ((-1, 0), (0, -1), (0, 1)),
    '╋': ((-1, 0), (1, 0), (0, -1), (0, 1)),
}


def connectedToWater(location, pipe, pipeMap):  # Checks for water sources at border of map
    if pipe != '.':
        for pipeDirection in pipeDict[pipe]:  # (pipeDirections)
            searchPos = [pipeDirection[0] + location[0], pipeDirection[1] + location[1]]
            if -1 in searchPos or searchPos[0] == len(pipeMap) or searchPos[1] == len(pipeMap[0]):
                return location


def findWaterSources(pipeMap):
    sources = []
    for rowIdx, row in enumerate(pipeMap):
        for colIdx, col in enumerate(row):
            if rowIdx == 0:
                sources.append(connectedToWater([rowIdx, colIdx], col, pipeMap))
            elif 0 > rowIdx < len(pipeMap) - 1:
                sources.append(connectedToWater([rowIdx, 0], col, pipeMap))
                sources.append(connectedToWater([rowIdx, -1], col, pipeMap))
            else:
                sources.append(connectedToWater([rowIdx, colIdx], col, pipeMap))
    return list(filter(None, sources))


#  Could be optimized
def checkFit(outgoingWaterDir: list, incomingWaterDir) -> bool:  # Adding the 2 directions should yield 0, 0
    logging.info(outgoingWaterDir)
    logging.info(incomingWaterDir)
    for pipeDirection in incomingWaterDir:
        if pipeDirection[0] + outgoingWaterDir[0] == 0:
            if pipeDirection[1] + outgoingWaterDir[1] == 0:
                return True
    return False


def recursiveSearch(source, pipeMap, lastPos, start, pipeRun) -> bool:
    pipeDirections = pipeDict[pipeMap[source[0]][source[1]]]
    for direction in pipeDirections:
        searchPos = [source[0] + direction[0], source[1] + direction[1]]
        if searchPos == lastPos:
            continue
        if 0 <= searchPos[0] < len(pipeMap) and 0 <= searchPos[1] < len(pipeMap[0]):
            logging.info(pipeMap[searchPos[0]][searchPos[1]])
            if pipeMap[searchPos[0]][searchPos[1]] == '.': return False
            if checkFit(direction, pipeDict[pipeMap[searchPos[0]][searchPos[1]]]):
                if searchPos in pipeRun:  # Loop found in pipe system
                    return True
                pipeRun.append(searchPos)  # Check for loops in pipeRun
                leakFree = recursiveSearch(searchPos, pipeMap, source, False, pipeRun)
                if not leakFree:  # Leak found
                    return leakFree
            else:
                return False  # Leak Found - Pipes do not fit.
        else:
            if start:
                leakFree = True
                start = False
                continue
            else:
                leakFree = True
    return leakFree


def check_pipe(pipe_map):
    pipeMap = [[x for x in row] for row in pipe_map]
    waterSources = findWaterSources(pipeMap)
    leakFree = True
    for source in waterSources:
        logging.info(pipeMap[source[0]][source[1]])
        leakFree = recursiveSearch(source, pipeMap, [-1, -1], start=True, pipeRun=[source])
        if not leakFree:
            break
    return leakFree


maps = [
    ['╋━━┓',
     '┃..┃',
     '┛..┣'],

    ['...┏',
     '┃..┃',
     '┛..┣'],

    ['...┏',
     '...┃',
     '┛..┣'],

    ['...┏',
     '...┃',
     '┓..┣'],

    ['╋',
     '╋',
     '╋'],

    ['╋....',
     '┃..┛.',
     '┃....'],

    ['....',
     '.┛┛.',
     '....'],
    ['━┻',
     '┏┓',
     '┃┃',
     '┣┛',
     '┣┓']
]
# Need to deal with loops
# r = check_pipe(maps[7])
# print(r)

for map in maps:
    r = check_pipe(map)
    print(r)
