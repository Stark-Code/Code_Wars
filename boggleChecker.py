class Answer:
    def __init__(self, result):
        self.a = result

    def getResult(self):
        return self.a

    def setResult(self, result):
        self.a = result


def searchSurroundingTiles(currPos, argBoard, word, argwordPath):
    solutions = []
    nextLetterIndex = len(argwordPath)
    print(f"Searching for {word[nextLetterIndex]} from {argBoard[currPos[0]][currPos[1]]} : {currPos}")

    searchList = []
    left, right = [currPos[0], currPos[1] - 1], [currPos[0], currPos[1] + 1]
    up, down = [currPos[0] - 1, currPos[1]], [currPos[0] + 1, currPos[1]]
    upLeft, upRight = [currPos[0] - 1, currPos[1] - 1], [currPos[0] - 1, currPos[1] + 1]
    downLeft, downRight = [currPos[0] + 1, currPos[1] - 1], [currPos[0] + 1, currPos[1] + 1]
    searchList.extend((left, right, up, down, upLeft, upRight, downLeft, downRight))

    for x in searchList:
        if 0 <= x[0] < len(argBoard) and 0 <= x[1] < len(argBoard[0]):
            if argBoard[x[0]][x[1]] == word[nextLetterIndex]:
                if x not in argwordPath:
                    solutions.append(x)

    return solutions


def recursiveSearch(wordPath, argBoard, word, answer):
    if len(wordPath) == len(word):
        print("Solution Found!")
        answer.setResult(True)
        return

    print(f"Search call: Current Path: {wordPath}")
    currPos = [wordPath[-1][0], wordPath[-1][1]]
    adjNodes = searchSurroundingTiles(currPos, argBoard, word, wordPath)

    if len(adjNodes) > 0:
        print(f"All surrounding nodes searched. Possible nodes: {adjNodes}")
        for i in range(len(adjNodes)):
            if len(wordPath) <= len(word):
                if i > 0:
                    # Remove Last Solution
                    if adjNodes[i - 1] in wordPath:
                        index = wordPath.index(adjNodes[i - 1])
                        wordPath = wordPath[:index]
                wordPath.append(adjNodes[i])
                print(f"Adding {adjNodes[i]} to path: New Path: {wordPath}")
                recursiveSearch(wordPath, argBoard, word, answer)
    else:
        removed = wordPath.pop()

        print(f"No path to next letter found from node: {removed}. Node removed from path")


def find_word(argBoard, word):
    wordPath = ""
    answer = Answer(False)
    for y in range(len(argBoard)):
        for x in range(len(argBoard[y])):
            if len(wordPath) < len(word):
                if argBoard[y][x] == word[0]:  # Letter Found
                    print(f"Letter found in driver function @ [{y, x}]")
                    wordPath = [[y, x]]
                    recursiveSearch(wordPath, argBoard, word, answer)
                    print(f"Test wordPath: {wordPath}")
    if answer.getResult():
        return True
    else:
        return False


board = [['L', 'H', 'A', 'R', 'R', 'G', 'A'],  # 0
         ['H', 'O', 'E', 'A', 'Y', 'C', 'L'],  # 1
         ['C', 'A', 'B', 'D', 'T', 'E', 'U'],  # 2
         ['C', 'N', 'A', 'Y', 'O', 'D', 'A'],  # 3
         ['R', 'O', 'K', 'T', 'L', 'I', 'R'],  # 4
         ['P', 'N', 'I', 'A', 'P', 'T', 'V'],  # 5
         ['G', 'M', 'S', 'E', 'M', 'R', 'S']  # 6
         ]
find_word(board, "HARR")

