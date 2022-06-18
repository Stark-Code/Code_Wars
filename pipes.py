import logging
import copy
logging.basicConfig(level=logging.INFO, format=' - %(message)s')

pipeDict2 = {
    '(0, 1)(0, 1)': '━',
    '(0, 1)(-1, 0)': '┛',
    '(-1, 0)(0, 1)': '┏',
    '(-1, 0)(-1, 0)': '┃',
    '(0, 1)(1, 0)': '┓',
    '(1, 0)(1, 0)': '┃',
    '(1, 0)(0, 1)': '┗'
}

pipeDict3 = {
    '(0, 1)(0, 1)': 9473,
    '(0, 1)(-1, 0)': 9499,
    '(-1, 0)(0, 1)': 9487,
    '(-1, 0)(-1, 0)': 9475,
    '(0, 1)(1, 0)': 9491,
    '(1, 0)(1, 0)': 9475,
    '(1, 0)(0, 1)': 9495
}


searchParams = [[-1, 0], [1, 0], [0, 1]]


def pipeToList(lawn):
    newPipeMap = []
    for pipeRow in lawn:
        newRow = []
        while pipeRow:
            newRow.append(pipeRow[:1])
            pipeRow = pipeRow[1:]
        newPipeMap.append(newRow)
        for coldIdx, col in enumerate(newPipeMap[-1]):
            if col == ".":
                newPipeMap[-1][coldIdx] = 0
    return newPipeMap


def findNext(currPos, pipes):
    for direction in searchParams:
        searchLoc = [currPos[0] + direction[0], currPos[1] + direction[1]]
        if 0 <= searchLoc[0] < len(pipes) and 0 <= searchLoc[1] < len(pipes[0]):
            if pipes[searchLoc[0]][searchLoc[1]] == 'x':
                return searchLoc


def connect_pipes(pipes, s, e):
    lastLoc = [s, -1]
    currLoc = [s, 0]
    finish = [e, len(pipes[e])]
    pipes = pipeToList(pipes)
    while True:
        logging.info(f'current Location: {currLoc}')
        nextLoc = findNext(currLoc, pipes)
        pathFrom = currLoc[0] - lastLoc[0], abs(lastLoc[1] - currLoc[1])
        if nextLoc is None:
            logging.info('Last element reached')
            logging.info(finish)
            logging.info(currLoc)
            pathTo = finish[0] - currLoc[0], abs(finish[1] - currLoc[1])
            pipes[currLoc[0]][currLoc[1]] = pipeDict3[str(pathFrom) + str(pathTo)]
            break
        # pathTo = nextLoc[0] - currLoc[0], abs(currLoc[1] - lastLoc[1]) 1
        pathTo = nextLoc[0] - currLoc[0], abs(nextLoc[1] - currLoc[1])  # 2
        pipes[currLoc[0]][currLoc[1]] = pipeDict3[str(pathFrom)+str(pathTo)]
        lastLoc = copy.copy(currLoc)
        currLoc = copy.copy(nextLoc)
        logging.info(f'pathFrom: {pathFrom}')
        logging.info(f'pathTo: {pathTo}')
    for row in pipes:
        print(row)
    return pipes


pipeMap1 = ['...',
            'xxx',
            '...']
pipeMap2 = ['.xxx',
            '.x.x',
            'xx.x',
            '...x'
            ]

pipeMap3 = ['xxxxxx']

r = connect_pipes(pipeMap3, 0, 0)
print(r)


'''
pipeMap1
step 1 = 0101
1,-1 ->1,0:  1 - 1 = 0; abs(-1-0) = 1
1,0 -> 1,1:  1 - 1 = 0; abs(0-1) = 1

step2 =
1,1 -> 1,2: 1-1 = 0; abs(1-2) = 1
1,2 -> 1,3: 1-1=0; abs(2-3) = 1
'''