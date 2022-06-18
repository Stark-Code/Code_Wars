class Spreader:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return 'S'

    def getLocation(self):
        return [self.row, self.col]

    def destroy(self):
        print(f'Spreader at {self.getLocation()} was destroyed!')
        del self


class Rifle:
    def __init__(self, row, col, attackRate):
        self.row = row
        self.col = col
        self.attackRate = int(attackRate)

    def __str__(self):
        return f'{self.attackRate}'

    def getLocation(self):
        return [self.row, self.col]

    def destroy(self):
        print(f"Rifle at {self.getLocation()} was destroyed!")
        del self


class Zombie:
    def __init__(self, row, col, hp):
        self.row = row
        self.col = col
        self.health = hp

    def __str__(self):
        return f'{self.health}'

    def getHealth(self):
        if self.health <= 0:
            print(f"Zombie at {self.getLocation()} has been killed!")
            self.destroy()
        return self.health

    def setHealth(self, attackPower):
        self.health -= int(attackPower)

    def setLocation(self, row, col):
        self.row, self.col = row, col

    def getLocation(self):
        return [self.row, self.col]

    def destroy(self):
        del self


def printLawn(step, lawn):
    print(f'Step: {step}')
    for rowIdx, row in enumerate(lawn):
        temp = []
        for col in row:
            temp.append(col.__str__())
        print(rowIdx, temp)


def lawnToList(lawn):
    newLawn = []
    for lawnRow in lawn:
        newRow = []
        while lawnRow:
            newRow.append(lawnRow[:1])
            lawnRow = lawnRow[1:]
        newLawn.append(newRow)
    for row in newLawn:
        row.append("*")
    return newLawn


def getSpawnTimes(zombies):
    spawnTimes = []
    for zombie in zombies:
        while len(spawnTimes) <= zombie[0]:
            spawnTimes.append([])
        spawnTimes[zombie[0]].append(zombie)
    return spawnTimes


def initGuns(lawn):
    for rowIdx, row in enumerate(lawn):
        for colIdx, col in enumerate(row):
            if col.isdigit():
                gun = Rifle(rowIdx, colIdx, int(col))
                lawn[rowIdx][colIdx] = gun
            elif col == "S":
                spreader = Spreader(rowIdx, colIdx)
                lawn[rowIdx][colIdx] = spreader
    return lawn


def updateZombies(lawn):
    for rowIdx, row in enumerate(lawn):
        for colIdx, col in enumerate(row):
            if isinstance(col, Zombie):
                zombie = col
                zombieLoc = zombie.getLocation()
                lawn[zombieLoc[0]][zombieLoc[1]] = " "  # Set last step to empty
                gunCheck = lawn[zombieLoc[0]][zombieLoc[1]-1]  # Check zombies next position for friendly
                if isinstance(gunCheck, Rifle) or isinstance(gunCheck, Spreader):
                    gunCheck.destroy()
                lawn[zombieLoc[0]][zombieLoc[1]-1] = zombie
                zombie.setLocation(rowIdx, colIdx-1)
    return lawn


def updateRifles(lawn):
    for rowIdx, row in enumerate(lawn):
        for colIdx, col in enumerate(row):
            if isinstance(col, Rifle):
                rifle, attackRate = col, col.attackRate
                while attackRate > 0:
                    bullet = rifle.getLocation()
                    bullet[1] += 1
                    while bullet[1] < len(lawn[0]):
                        if isinstance(lawn[bullet[0]][bullet[1]], Zombie):
                            zombie = lawn[bullet[0]][bullet[1]]
                            zombie.setHealth(1)
                            if zombie.getHealth() <= 0:
                                lawn[bullet[0]][bullet[1]] = " "
                            break
                        else:
                            bullet[1] += 1
                    attackRate -= 1
    return lawn


def updateSpreaders(lawn):
    for col in range(len(lawn[0])-1, -1, -1):
        for row in range(len(lawn)):
            if isinstance(lawn[row][col], Spreader):
                spreader = lawn[row][col]

                for shot in range(3):  # 3 way shot
                    bullet = spreader.getLocation()
                    if shot == 0:  # upRight
                        bulletDir = (-1, 1)
                    elif shot == 1:  # right
                        bulletDir = (0, 1)
                    else:  # downRight
                        bulletDir = (1, 1)
                    bullet[0] += bulletDir[0]
                    bullet[1] += bulletDir[1]

                    while 0 <= bullet[0] < len(lawn) and bullet[1] < len(lawn[0]):  # Bullet travel loop
                        if isinstance(lawn[bullet[0]][bullet[1]], Zombie):
                            zombie = lawn[bullet[0]][bullet[1]]
                            zombie.setHealth(1)
                            if zombie.getHealth() <= 0:
                                lawn[bullet[0]][bullet[1]] = " "
                            break
                        else:
                            bullet[0] += bulletDir[0]
                            bullet[1] += bulletDir[1]
    return lawn


def checkForZombieWin(lawn):
    for rowIdx in range(len(lawn)):  # Check column 0 for zombies
        if isinstance(lawn[rowIdx][0], Zombie) and lawn[rowIdx][0].getHealth() > 0:
            print("Zombies have won!")
            return True


def checkGameOver(lawn):
    for row in lawn:  # Check lawn for zombies
        for col in row:
            if isinstance(col, Zombie) and col.getHealth() > 0:
                print("Zombies still active")
                return False
    return "Zombies lose"


def plants_and_zombies(lawn, zombies):
    lawn = lawnToList(lawn)
    spawnTimes = getSpawnTimes(zombies)
    zombieSpawnCol = len(lawn[0]) - 1
    step = 0
    lawn = initGuns(lawn)  # Load map with gun objects

    while True:  # Main Loop
        for spawn in spawnTimes:
            for zombie in spawn:  # Spawn zombies at each game step
                zombie = Zombie(zombie[1], zombieSpawnCol, zombie[2])
                zombieLoc = zombie.getLocation()
                lawn[zombieLoc[0]][zombieLoc[1]] = zombie
            lawn = updateZombies(lawn)
            lawn = updateRifles(lawn)
            lawn = updateSpreaders(lawn)
            printLawn(step, lawn)
            step += 1
            zombieWin = checkForZombieWin(lawn)  # Check if zombies have overtaken base at end of turn
            if zombieWin:
                return step

        gameOver = checkGameOver(lawn)
        if gameOver == "Zombies lose":
            return None
        spawnTimes = [[[0, 0, 0]]]  # Hack to keep game running until gameOver
        

lawn1 = [
           '2       ',
           '  S     ',
           '21  S   ',
           '13      ',
           '2 3     ']
lawn2 = ['4        ', 'S5       ', '51S1     ', '24 1     ', '22S1     ', '22S1     ']
lawn = [
    '1         ',
    'SS        ',
    'SSS       ',
    'SSS       ',
    'SS        ',
    '1         '
]
zombies1 = [[0, 4, 28], [1, 1, 6], [2, 0, 10], [2, 4, 15], [3, 2, 16], [3, 3, 13]]
zombies2 = [[1, 1, 24], [1, 3, 28], [1, 4, 24], [1, 5, 24], [3, 0, 18], [3, 4, 16], [3, 5, 16], [4, 2, 39], [4, 3, 22], [6, 2, 25], [6, 4, 14], [6, 5, 14], [7, 1, 24], [7, 2, 18], [7, 3, 18], [8, 0, 17], [8, 1, 16], [8, 4, 13], [8, 5, 13], [9, 2, 17], [10, 0, 13], [10, 1, 14], [10, 3, 19], [11, 2, 16], [11, 4, 15], [12, 0, 10]]
zombies3 = zombies = [[0,2,16],[1,3,19],[2,0,18],[4,2,21],[6,3,20],[7,5,17],[8,1,21],[8,2,11],[9,0,10],[11,4,23],[12,1,15],[13,3,22]]

r = plants_and_zombies(lawn, zombies3)
print(f"Result: {r}")