import copy
import sys


class Alien:
    def __init__(self, wave, col, speed, direction):
        self.row = wave
        self.col = col
        self.speed = speed
        self.direction = direction
        self.name = f'{col}'

    def __str__(self):
        return self.name

    def destroy(self):
        del self

    def findNextPosition(self, board):
        # print(f'Alien {self.name} is moving!')
        speedCopy = copy.copy(self.speed)
        speedCopy -= 1
        while speedCopy >= 0:
            if self.direction == -1:
                if self.col > 0:
                    self.col -= 1
                    speedCopy -= 1
                else:
                    self.row += 1
                    speedCopy -= 1
                    self.direction *= -1
            elif self.direction == 1:
                if self.col < board[1] - 1:
                    self.col += 1
                    speedCopy -= 1
                else:
                    self.row += 1
                    speedCopy -= 1
                    self.direction *= -1
        # print(f'New position {self.row, self.col}!')
        return [self.row, self.col]  # For debugging

    def checkAttacked(self, attackRow, attackColumn):
        if self.row == attackRow and self.col == attackColumn:
            print(f"Alien at {self.row, self.col} is in the cross hairs!")
            return True


def printBoard(board, playerPos):
    for rowIdx, row in enumerate(board):
        temp = []
        for col in row:
            if isinstance(col, list):
                double = ""
                for ship in col:
                    double += "." + ship.__str__()
                temp.append(double)
            else:
                temp.append(col.__str__())
        print(rowIdx, temp)
    print(f"{'        ' * playerPos[1]} ^ ")


def prioritizeTarget(alien):
    print(f"Sort {alien}, {alien.speed}")
    return abs(alien.speed)


def populateAliens(aliens):
    alienTracker = []
    for waveIdx, wave in enumerate(aliens):
        # print(f"Step : {step}")
        # step += 1
        for invaderIdx, invader in enumerate(wave):
            if invader != 0:
                newInvader = Alien(waveIdx, invaderIdx, abs(invader), invader / abs(invader))
                alienTracker.append(newInvader)
    return alienTracker


def blast_sequence(aliens, position):
    boardDimensions = position[0], len(aliens[0])  # y, x
    attackColumn = position[1]
    alienTracker = []
    aliensUnderAttack = []
    totalWaves = len(aliens)
    step, shot, shotTracker = 0, 0, []
    alienTracker = populateAliens(aliens)

    while True:  # Main loop
        print(f"Step: {step}")
        board = [["--" for _ in range(boardDimensions[1])] for _ in range(boardDimensions[0] + 1)]  # For debugging
        for alien in alienTracker:  # Positions ships
            alienPosition = alien.findNextPosition(boardDimensions)  # Moves alien position
            # if board[alienPosition[0]][alienPosition[1]] != "--":
            #     if isinstance(board[alienPosition[0]][alienPosition[1]], list):
            #         temp = board[alienPosition[0]][alienPosition[1]]
            #         temp.append(alien)
            #         board[alienPosition[0]][alienPosition[1]] = temp
            #     else:
            #         board[alienPosition[0]][alienPosition[1]] = [board[alienPosition[0]][alienPosition[1]], alien]
            # else:
            #     board[alienPosition[0]][alienPosition[1]] = alien  # Place alien in new position (For debugging)

        for rowIdx in range(len(board) - 2, -1, -1):
            for alien in alienTracker:  # Looks through all aliens by row
                underAttack = alien.checkAttacked(rowIdx, attackColumn)
                if underAttack:
                    aliensUnderAttack.append(alien)
            if len(aliensUnderAttack) > 0:  # If aliens found at row, stop search and attack
                if len(aliensUnderAttack) > 1:
                    aliensUnderAttack.sort(reverse=True, key=prioritizeTarget)
                for alien in aliensUnderAttack:  # For debugging
                    print(f'Target found: id: {alien.__str__()}')

                # Attack alien with highest priority and record shot

                alienTracker.pop(alienTracker.index(aliensUnderAttack[0]))
                print(f'Alien {aliensUnderAttack[0].__str__()} destroyed!')
                aliensUnderAttack[0].destroy()
                print(f'Shot {step} being added to shot Tracker')
                shotTracker.append(step)
                aliensUnderAttack = []
                break
        step += 1
        printBoard(board, position)

        # Check for game over conditions
        print(f"Aliens remaining: {len(alienTracker)}, Total waves: {totalWaves} ")
        if len(alienTracker) == 0:  # All aliens defeated
            print("All aliens defeated!")
            break
        for alien in alienTracker:  # Alien has arrived at base
            if alien.row == position[0]:
                print("Aliens have taken over!")
                break

        # aliens = [[]]

    return shotTracker

#
# aliens1 = [[3, 1, 2, -2, 2, 3, 6, -3, 7, 1]]
# position1 = [6, 4]
# aliens2 = [[5, 2, -2, 3, 1, 0, 4, 8, 3, -2, 5], [1, 4, -1, 0, 3, 6, 1, -3, 1, 2, -4]]
# position2 = [10, 2]

aliens3 = [[3, 1, 2, -2, 2, 3, 6, -3, 7, 1]]
position3 = [6, 4]


# r = blast_sequence(aliens3, position3)
# print(r)

# [1,4,5,6,8,9,10,12,14,15,16,18,19,20,21,26,27,30,32,36]

s = [1, 6, -1, 2, -3, -5, 5, -6]
s.sort(reverse = True, key=lambda i: (abs(i), i))
print(s)