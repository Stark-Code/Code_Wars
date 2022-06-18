import copy


class Alien:
    def __init__(self, wave, col, speed):
        self.row = wave
        self.col = col
        self.speed = speed
        self.name = f'{col}'

    def __str__(self):
        return self.name

    def destroy(self):
        del self

    def findNextPosition(self, bD):  # bD: boardDimensions[1] = width of board-1
        speedCopy = copy.copy(self.speed)

        self.col += speedCopy
        if self.col > bD:
            overShot = self.col - bD - 1
            self.row += 1  # Subtracts 1 from overshot (above)
            self.col = bD - overShot
            self.speed *= -1
        elif self.col < 0: # Working on this
            overShot = 0 - self.col - 1
            self.row += 1
            self.col = overShot
            self.speed *= -1

    def checkAttacked(self, attackRow, attackColumn):
        if self.row == attackRow and self.col == attackColumn:
            return True


def populateAliens(aliens):
    alienTracker = []
    for waveIdx, wave in enumerate(aliens):
        for invaderIdx, invader in enumerate(wave):
            if invader != 0:
                newInvader = Alien(waveIdx, invaderIdx, invader)
                alienTracker.append(newInvader)
    return alienTracker


def blast_sequence(aliens, position):
    boardDimensions = position[0], len(aliens[0]) -1  # y, x
    attackColumn = position[1]
    aliensUnderAttack = []
    step, shotTracker = 0, []
    alienTracker = populateAliens(aliens)
    gameOver = False
    while not gameOver:  # Main loop
        for alien in alienTracker:  # Positions ships
            alien.findNextPosition(boardDimensions[1])  # Moves alien position

        for rowIdx in range(position[0]-1, -1, -1):
            for alien in alienTracker:  # Looks through all aliens by row
                underAttack = alien.checkAttacked(rowIdx, attackColumn)
                if underAttack:
                    aliensUnderAttack.append(alien)

            if len(aliensUnderAttack) > 0:  # If aliens found at row, stop search and attack
                if len(aliensUnderAttack) > 1:
                    aliensUnderAttack.sort(reverse=True, key=lambda alien: (abs(alien.speed), alien.speed))

                alienTracker.pop(alienTracker.index(aliensUnderAttack[0]))
                aliensUnderAttack[0].destroy()
                shotTracker.append(step)
                aliensUnderAttack = []
                break
        step += 1

        # Check for game over conditions
        if len(alienTracker) == 0:  # All aliens defeated
            gameOver = True
            break
        for alien in alienTracker:  # Alien has arrived at base
            if alien.row == position[0]:
                shotTracker = None
                gameOver = True
                break

    return shotTracker



aliens3 = [[3, 1, 2, -2, 2, 3, 6, -3, 7, 1]]
position3 = [6, 4]

r = blast_sequence(aliens3, position3)
print(r)
