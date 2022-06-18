import logging

searchParams = [[0, -1], [-1, 0], [0, 1], [1, 0]]
logging.basicConfig(level=logging.INFO,  format=' - %(message)s')


def printHeightMap(heightmap):
    for row in heightmap:
        temp = []
        for col in row:
            if isinstance(col, container):
                temp.append(col.__str__())
            else:
                temp.append(col)
        logging.info(temp)
    print('')
    for row in heightmap:
        for col in row:
            if isinstance(col, container):
                logging.info(col.location)
                logging.info(f'Group: {col.group}')


class container:
    def __init__(self, location, group):
        self.location = location
        self.group = group
        self.waterLevel = 0

    def __str__(self):
        return "w"

    def searchAdjacent(self, heightmap):
        global searchParams
        length, width = len(heightmap), len(heightmap[0])  # Can be optimized
        for direction in searchParams:
            searchPos = [self.location[0] + direction[0], self.location[1] + direction[1]]
            if 0 <= searchPos[0] < length and 0 <= searchPos[1] < width:
                if heightmap[searchPos[0]][searchPos[1]] == 0:
                    heightmap[searchPos[0]][searchPos[1]] = container([searchPos[0], searchPos[1]], self.group)


def volume(heightmap: list) -> int:
    group = 1
    for rowIdx, row in enumerate(heightmap):
        for colIdx, height in enumerate(row):
            if height == 0:
                newContainer = container([rowIdx, colIdx], group)
                heightmap[rowIdx][colIdx] = newContainer
                newContainer.searchAdjacent(heightmap)
                group += 1
                printHeightMap(heightmap)
            elif isinstance(height, container):
                existingContainer = height
                existingContainer.searchAdjacent(heightmap)
                printHeightMap(heightmap)
    return 1

hM = [[8, 8, 8, 8, 6, 6, 6, 6],
      [8, 0, 0, 8, 6, 0, 0, 6],
      [8, 0, 0, 8, 6, 0, 0, 6],
      [8, 8, 8, 8, 6, 6, 6, 0]]
volume(hM)  # 56
