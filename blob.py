import math


def buildBoard(mapDimensions):
    if len(mapDimensions) == 1:
        mapDimensions = [mapDimensions[0], mapDimensions[0]]
    return [["." for _ in range(mapDimensions[1])] for _ in range(mapDimensions[0])]


class Blob:
    def __init__(self, y, x, size):
        self.x, self.y = x, y
        self.size = size
        self.attackPos = []

    def __str__(self):
        return str(self.size)

    def findClosestBlob(self, blobList):
        minBlobDist = float('inf')
        largestBlob = 0
        for blob in blobList:
            yDist, xDist = abs(self.y - blob.y), abs(self.x - blob.x)
            distance = max(yDist, xDist)
            if blob.size < self.size:
                if 0 < distance < minBlobDist:  # Needs to be greater than zero or blob is attacking itself
                    blobsInRange = [blob]  # Reset because a closer blob was found
                    minBlobDist = distance
                    largestBlob = blob.size  # Reset because a closer blob was found
                elif distance == minBlobDist:
                    blobsInRange.append(blob)
                    if blob.size > largestBlob: largestBlob = blob.size
        return blobsInRange, largestBlob

    def moveTowardsBlob(self, location):
        if self.y < location[0]: self.y += 1
        elif self.y > location[0]: self.y -= 1
        if self.x < location[1]: self.x += 1
        elif self.x > location[1]: self.x -= 1

    def angleSort(self, e):
        rad = math.atan2(self.y - e.y, self.x - e.x)
        degrees = int(math.degrees(rad))
        if degrees == 90: return 1
        elif degrees > 90 and degrees < 180: return 2
        elif degrees == 180: return 3
        elif degrees < -90: return 4
        elif degrees == -90: return 5
        elif degrees > -90 and degrees < 0: return 6
        elif degrees == 0: return 7
        elif degrees > 0 and degrees < 90: return 8

    def move(self, blobList):  # Sorts blobs that the larger blob wants to attack
        blobsInRange, largestBlob = self.findClosestBlob(blobList)  # Filters attack by closest distance
        largestBlobs = []
        for blob in blobsInRange:
            if blob.size == largestBlob:  # Filters attack by larger size blobs
                largestBlobs.append(blob)
        largestBlobs.sort(key=self.angleSort)
        return [largestBlobs[0].y, largestBlobs[0].x]


def validateBlobData(blobData, height, width):
    for blobInfo in blobData:
        if 'x' not in blobInfo or isinstance(blobInfo['x'], bool) or blobInfo['x'] >= height or blobInfo['x'] < 0: return False
        if 'y' not in blobInfo or isinstance(blobInfo['y'], bool) or blobInfo['y'] >= width  or blobInfo['y'] < 0: return False
        if 'size' not in blobInfo or isinstance(blobInfo['size'], bool) or blobInfo['size'] <= 0 or blobInfo[
            'size'] > 20: return False
    return True


class Blobservation:
    def __init__(self, *args):
        self.boardDimensions = args
        self.board = buildBoard(self.boardDimensions)
        self.blobData = []

    def updateBoard(self, blobData: list):
        for blob in blobData:
            if isinstance(self.board[blob.y][blob.x], Blob):  # Blob absorbs another blob
                blob.size += self.board[blob.y][blob.x].size
                self.board[blob.y][blob.x] = blob
            else:
                self.board[blob.y][blob.x] = blob

    def populate(self, blobData, source='populate'):
        if validateBlobData(blobData, len(self.board), len(self.board[0])):
            newBlobs = [Blob(blob['x'], blob['y'], blob['size']) for blob in blobData]
            self.updateBoard(newBlobs)
        else:
            raise ValueError

    def move(self, *args):
        if len(args) == 0: rounds = 1
        elif not isinstance(args[0], bool): rounds = args[0]
        else: raise ValueError
        if rounds <= 0: raise ValueError
        while rounds:
            blobList = []
            minSize = float('inf')
            for row in self.board:
                for _blob in row:
                    if isinstance(_blob, Blob):
                        if _blob.size < minSize: minSize = _blob.size
                        blobList.append(_blob)
            if len(blobList) < 2: break
            for _blob in blobList:
                if _blob.size > minSize:  # If blob is bigger than minimum, it is allowed to attack
                    _blob.attackPos = _blob.move(blobList)  # Gets data on where a blob wants to move for attack
            blobData = []
            for _blob in blobList:
                blobData.append(_blob)
                if _blob.size > minSize:
                    _blob.moveTowardsBlob(_blob.attackPos)  # Moves blobs of qualifying size
            self.board = buildBoard(self.boardDimensions)
            self.updateBoard(blobData)
            rounds -= 1

    def print_state(self):
        blobStates = []
        for yIdx, row in enumerate(self.board):
            for xIdx, col in enumerate(row):
                if isinstance(col, Blob):
                    blobStates.append([col.y, col.x, col.size])
        return blobStates
