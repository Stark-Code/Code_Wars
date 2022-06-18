import re

class Position:
    def __init__(self):
        self.position = [0, 0]
        self.orientation = [-1, 0]

    def getPositionalData(self):
        return self.position, self.orientation

    def setPosition(self, position):
        self.position = position

    def setOrientation(self, orientation):
        self.orientation = orientation


player = Position()


def encodePath(path):
    idx = 0
    route = []

    while idx < len(path):
        elem = ""
        if path[idx].isalpha():
            elem = path[idx]
            idx += 1
        elif path[idx].isnumeric():
            elem = path[idx]
            idx += 1
            if idx < len(path):
                while path[idx].isnumeric():
                    elem += path[idx]
                    idx += 1
                    if idx < len(path):
                        continue
                    else:
                        break
        route.append(elem)

    return route


def i_am_here(path):
    if path == '':
        return [0, 0]
    route = re.findall(r'\d+|.', path)
    # route = encodePath(path)
    print(route)
    playerData = player.getPositionalData()  # position, orientation
    print(f"playerDataStart: {playerData}")
    for command in route:
        if command == 'r':
            if playerData[1][0] == -1: # Up
                playerData[1][0] = 0
                playerData[1][1] = 1
            elif playerData[1][0] == 1: # Down
                playerData[1][0] = 0
                playerData[1][1] = -1
            elif playerData[1][1] == 1: # Right
                playerData[1][0] = 1
                playerData[1][1] = 0
            elif playerData[1][1] == -1:
                playerData[1][0] = -1
                playerData[1][1] = 0
        if command == 'l':
            if playerData[1][0] == -1: # Up
                playerData[1][0] = 0
                playerData[1][1] = -1
            elif playerData[1][0] == 1: # Down
                playerData[1][0] = 0
                playerData[1][1] = 1
            elif playerData[1][1] == 1: # Right
                playerData[1][0] = -1
                playerData[1][1] = 0
            elif playerData[1][1] == -1:
                playerData[1][0] = 1
                playerData[1][1] = 0
        if command == "R" or command == "L":
            playerData[1][0] *= -1
            playerData[1][1] *= -1
        if command.isnumeric():
            intCommand = int(command)
            movementY = playerData[1][0] * intCommand
            movementX = playerData[1][1] * intCommand
            playerData[0][0] += movementY
            playerData[0][1] += movementX
        print(f"Command {command} applied. Pos: {playerData[0]} Dir: {playerData[1]} ")
        player.setPosition(playerData[0])
        player.setOrientation(playerData[1])
    print(f"Result: {playerData}")
    return playerData[0]
# position = [0, 0] # y, x
# orientation [-1, 0]
# orientation + r = [0, 1] turn off 1,
# orientation + L = [0, -1]
# R, L flips 1 value
# r, l turns off value, and adds the opposite of that turned off value to other element

# i_am_here("rr5l90Rl86r53RR79R78l69r96r31r")
# i_am_here("R2R2L2R")
i_am_here('r5L2l4')
# 'r5L2l4', [4, 3])

# r = 90 >
# L = 180
#
# -1, 0
# 1, ,0
# 0, 1
# 0, -1

#  If Im facing up or down l and r have difference effects. Code does not account for this.
