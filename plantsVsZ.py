import time
import sys


class Spreader:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def getLocation(self):
        return self.row, self.col

    def shoot(self):
        pass

    def destroy(self):
        del self


class Rifle:
    def __init__(self, row, col, attackRate):
        self.row = row
        self.col = col
        self.attackRate = int(attackRate)

    def getLocation(self):
        return self.row, self.col

    def getAttackRate(self):
        return self.attackRate

    def destroy(self):
        del self


class Zombie:
    def __init__(self, row, col, hp):
        self.row = row
        self.col = col
        self.health = hp

    def setHealth(self, attackPower):
        self.health -= int(attackPower)

    def getHealth(self):
        return self.health

    def setLocation(self):
        self.col -= 1

    def getLocation(self):
        return self.row, self.col

    def destroy(self):
        del self


def lawnToList(lawn):
    newLawn = []
    for lawnRow in lawn:
        newRow = []
        while lawnRow:
            newRow.append(lawnRow[:1])
            lawnRow = lawnRow[1:]
        newLawn.append(newRow)
    print("Step -1")
    for row in newLawn:
        row.append("*")
        print(row)
    return newLawn


def getSpawnTimes(zombies):
    spawnTimes = []
    for zombie in zombies:
        while len(spawnTimes) <= zombie[0]:
            spawnTimes.append([])
        spawnTimes[zombie[0]].append(zombie)
    return spawnTimes


def initShooters(lawn):
    rifles = []
    spreaders = []
    for rowIdx, row in enumerate(lawn):
        for colIdx, col in enumerate(row):
            if col != " ":
                if col == "S":
                    spreader = Spreader(rowIdx, colIdx)
                    spreaders.append(spreader)
                elif col != "*":
                    rifle = Rifle(rowIdx, colIdx, col)
                    rifles.append(rifle)
    return rifles, spreaders


def updateLivingZombies(lawn, livingZombies):
    for zombie in livingZombies:
        zombieHealth = zombie.getHealth()
        zombieLoc = zombie.getLocation()
        lawn[zombieLoc[0]][zombieLoc[1]] = zombieHealth
    return lawn


def updateGunShots(lawn, livingZombies, rifles, spreaders):
    # Rifles shoot first
    for rifle in rifles:
        rifleAttackRate = rifle.getAttackRate()
        rifleLoc = rifle.getLocation()
        zombiesInAttackZone = []
        # Find zombies in attack zone of rifle
        for zombie in livingZombies:
            zombieLoc = zombie.getLocation()
            if zombieLoc[0] == rifleLoc[0]:
                zombiesInAttackZone.append(zombie)
        if len(zombiesInAttackZone) == 0:
            continue

        while rifleAttackRate > 0:
            rifleAttackRate -= 1
            if len(zombiesInAttackZone) == 0:
                continue
            zombiesInAttackZone[0].setHealth(1)  # Attack Zombie

            # print(f'Zombie at location {zombiesInAttackZone[0].getLocation()} was attacked!')
            if zombiesInAttackZone[0].getHealth() <= 0:
                print('A zombie has been killed!')
                zombieLoc = zombiesInAttackZone[0].getLocation()
                lawn[zombieLoc[0]][zombieLoc[1]] = " "
                livingZombies.pop(livingZombies.index(zombiesInAttackZone[0]))
                zombiesInAttackZone[0].destroy()  # Might not work well
                zombiesInAttackZone.pop(0)  # Redundant?
                lawn = updateLivingZombies(lawn, livingZombies)
    # Spreaders shoot in order from right to left, then top to bottom
    # Find spreader priority
    spreaderPriority = []
    # for col in range(len(test[0]) - 1, -1, -1):
    #     for row in range(len(test[0])):
    #         print(test[row][col])
    for _col in range(len(lawn[0])-1, 0, -1):
        for _row in range(len(lawn)-1, 0, -1):
            if lawn[_row][_col] == "S":
                for spreader in spreaders:
                    spreaderLoc = spreader.getLocation()
                    if spreaderLoc == (_row, _col):
                        spreaderPriority.append(spreader)
    for spreader in spreaderPriority:
        spreaderLoc = spreader.getLocation()
        print(f'There is a spreader at {spreaderLoc}')
    for spreader in spreaderPriority:
        print(f'Checking spreader at {spreader.getLocation()}')
        spreaderLoc = spreader.getLocation()
        zombiesInSpreaderForwardAttackZone = []
        # Find zombies in attack zone in front of spreader
        for zombie in livingZombies:
            zombieLoc = zombie.getLocation()
            if zombieLoc[0] == spreaderLoc[0]:
                zombiesInSpreaderForwardAttackZone.append(zombie)
        if len(zombiesInSpreaderForwardAttackZone) > 0:
            zombiesInSpreaderForwardAttackZone[0].setHealth(1)
            print('A zombie was hit by a forward spreader bullet')

        # Check upRight
        bulletLocation = list(spreaderLoc)
        bulletActive = True
        while bulletActive:
            bulletLocation[0] -= 1
            bulletLocation[1] += 1
            if bulletLocation[0] >= 0 and bulletLocation[1] <= len(lawn[0]) - 2:
                for zombie in livingZombies:
                    zombieLoc = zombie.getLocation()
                    # print(f"{list(zombieLoc)} ==? {bulletLocation}")
                    if list(zombieLoc) == bulletLocation:
                        print(f'A zombie at {zombieLoc} was hit by an upRight bullet')
                        zombie.setHealth(1)
                        bulletActive = False
                        break
            else:
                bulletActive = False

        # check downRight
        bulletLocation = list(spreaderLoc)
        bulletActive = True
        while bulletActive:
            bulletLocation[0] += 1
            bulletLocation[1] += 1
            if bulletLocation[0] < len(lawn) and bulletLocation[1] <= len(lawn[0]) - 2:
                for zombie in livingZombies:
                    zombieLoc = zombie.getLocation()
                    # print(f"{list(zombieLoc)} ==? {bulletLocation}")
                    if list(zombieLoc) == bulletLocation:
                        print(f'A zombie at {zombieLoc} was hit by an downRight bullet')
                        zombie.setHealth(1)
                        bulletActive = False
                        break
            else:
                bulletActive = False

        # Updating zombie health after 3 bullets have become inactive
        for zombie in livingZombies:
            if zombie.getHealth() <= 0:
                print('A zombie has been killed!')
                zombieLoc = zombie.getLocation()
                lawn[zombieLoc[0]][zombieLoc[1]] = " "
                livingZombies.pop(livingZombies.index(zombie))
                zombie.destroy()  # Might not work well
        # Updating map
        lawn = updateLivingZombies(lawn, livingZombies)

    return lawn, livingZombies


def updateZombieProgress(lawn, livingZombies, rifles, spreaders):
    for zombie in livingZombies:
        zombieLoc = zombie.getLocation()  # Old Zombie Location
        if lawn[zombieLoc[0]][zombieLoc[1]] != "*":
            lawn[zombieLoc[0]][zombieLoc[1]] = ' '
        zombie.setLocation()
        zombieLoc = zombie.getLocation()  # New Zombie Location
        if lawn[zombieLoc[0]][zombieLoc[1]] == "S":  # Zombie attacks a spreader
            for spreader in spreaders:
                spreaderLoc = spreader.getLocation()
                if spreaderLoc == zombieLoc:
                    print(f'A zombie has overtaken a spreader at {spreaderLoc}')
                    spreaders.pop(spreaders.index(spreader))
                    spreader.destroy()
        elif lawn[zombieLoc[0]][zombieLoc[1]] != ' ':  # Zombie attacks a rifle
            for rifle in rifles:
                rifleLoc = rifle.getLocation()
                if rifleLoc == zombieLoc:
                    print(f"A zombie has overtaken a rifle at {rifleLoc}")
                    rifles.pop(rifles.index(rifle))
                    rifle.destroy()
        zombieHealth = zombie.getHealth()
        lawn[zombieLoc[0]][zombieLoc[1]] = str(zombieHealth)
    return lawn, rifles, spreaders


def plants_and_zombies(lawn, zombies):
    lawn = lawnToList(lawn)
    rifles, spreaders = initShooters(lawn)
    livingZombies = []

    spawnTimes = getSpawnTimes(zombies)
    gameOver = False
    step = 0
    #  main loop
    while True:
        for spawn in spawnTimes:  # Main Step
            print(f'Step: {step}')
            for zombie in spawn:  # Spawn zombies at each game step
                zombie = Zombie(zombie[1], zombieSpawnCol, zombie[2])
                if zombie.getHealth() > 0:
                    livingZombies.append(zombie)
            lawn, rifles, spreaders = updateZombieProgress(lawn, livingZombies, rifles,
                                                           spreaders)  # Walk zombies and attack
            # for zombie in livingZombies:
            #     if zombie.getLocation()[1] == 0:
            #         livingZombies.pop(livingZombies.index(zombie))
            #         sys.exit()
            lawn, livingZombies = updateGunShots(lawn, livingZombies, rifles, spreaders)  # Fire artillery

            step += 1
            for rowIdx, row in enumerate(lawn):
                print(rowIdx, row)
            print('    0', '   1', '   2', '   3', '   4', '   5', '   6', '   7', '   8')
        spawnTimes = [[[0, 0, 0]]]

        if len(livingZombies) == 0:
            break

        for zombie in livingZombies:
            zombieLoc = zombie.getLocation()
            if zombieLoc[1] == 0:
                gameOver = True
                break
        if gameOver:
            break
    if len(livingZombies) == 0:
        return None
    else:
        return step
lawn = ['2121                ', '6    S              ', '3 2  S              ', '22 S S              ', '2 1 2S              ', '311                 ']
z = [[0, 4, 49], [0, 0, 88], [0, 1, 92], [0, 2, 75], [1, 5, 69], [1, 3, 78], [3, 1, 24], [4, 2, 18], [4, 5, 21], [6, 0, 51], [7, 4, 59], [7, 1, 29], [10, 2, 34], [11, 5, 37], [11, 1, 42], [13, 0, 44], [13, 3, 33], [13, 2, 59], [15, 1, 54], [16, 0, 24], [16, 2, 42], [17, 5, 36], [18, 3, 48], [18, 4, 39], [19, 2, 85]]

lawn1 = ['4S 1    ', 'S4      ', '11 1    ', '21 2    ', 'S4      ']
z1 = [[0, 1, 18], [0, 3, 18], [0, 4, 18], [1, 0, 24], [1, 1, 12], [1, 3, 12], [1, 4, 12], [2, 2, 13], [4, 0, 18], [4, 1, 11], [4, 2, 9], [4, 4, 11], [5, 2, 6], [6, 1, 10], [6, 3, 15], [7, 3, 11], [7, 4, 13], [8, 0, 21], [8, 2, 7], [8, 4, 9], [9, 0, 14], [9, 2, 5], [9, 3, 10], [11, 0, 11], [11, 1, 15], [11, 4, 9], [12, 2, 6], [12, 3, 10], [15, 0, 14], [15, 1, 15], [15, 3, 10], [15, 4, 12], [17, 1, 10], [17, 2, 7], [17, 4, 9], [18, 0, 13], [18, 2, 5]]

tic = time.perf_counter()
plants_and_zombies(lawn1, z1)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")


