def buildMaze(maze):
    mx, c, mm = [], [], ""
    for x in maze:
        mm += x
        if x == '\n':
            mm = mm[:-1]
            mx.append(mm)
            mm = ""
    mx.append(mm)
    for x in range(len(mx)):
        c.append([])
        for y in range(len(mx[x])):
            c[-1].append(mx[x][y])
        c[0][0] = "1"
    return c


def searchAdj(currPos, maze):  # [y, x]
    nextStep = int(maze[currPos[0]][currPos[1]]) + 1
    searchList = []
    left, right = [currPos[0], currPos[1] - 1], [currPos[0], currPos[1] + 1]
    up, down = [currPos[0] - 1, currPos[1]], [currPos[0] + 1, currPos[1]]
    searchList.extend((left, right, up, down))
    nextNodes = []
    for x in searchList:
        if 0 <= x[0] < len(maze) and 0 <= x[1] < len(maze[0]) and maze[x[0]][x[1]] == ".":
            maze[x[0]][x[1]] = str(nextStep)
            nextNodes.append([x[0], x[1]])
    return nextNodes


def path_finder(maze):

    maze = buildMaze(maze)
    answer = False

    def re(maze, path, argAnswer):
        if maze[-1][-1] != ".":
            print("Solution Found!")
            argAnswer = maze[-1][-1]
            return argAnswer
        if len(path) == 0:
            argAnswer = False
            return argAnswer
        nextPath = []
        for i in path:
            nextPath += searchAdj(i, maze)
            print(f"Next: {path}")
        for row in maze:
            print(row)
        return re(maze, nextPath, argAnswer)

    answer = re(maze, [[0, 0]], answer)
    return answer


d = "\n".join(["......",
               "......",
               "......",
               "......",
               ".....W",
               "...W.."])
path_finder(d)
