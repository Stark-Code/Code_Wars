import sys
import time
import re
from copy import deepcopy
from colorama import init, Back

init(autoreset=True)


class Alien:
    def __init__(self, health):
        self.position = 0
        self.gridLocation = None
        self.health = health
        self.alienID = None

    def __str__(self):
        return f'{str(self.alienID)}:{self.health}'

    def setID(self, _id):
        self.alienID = _id

    def setOrigin(self, origin):
        self.gridLocation = origin


class Turret:
    def __init__(self, name, location, attackRange, ammo):
        self.name = name
        self.location = location
        self.attackRange = attackRange
        self.ammo = ammo
        self.attackSquares = []
        self.ammoCapacity = deepcopy(ammo)

    def __str__(self):
        return f'{self.name} @ ({self.location} Range: {self.attackRange}, Rate: {self.ammo}, ' \
               f'AttackSquares: {self.attackSquares} '

    def reload(self):
        self.ammo = self.ammoCapacity

    def defineAttackSquares(self, alienPath):
        for node in reversed(alienPath):
            distFromTurret = abs(self.location[0] - node[0]) + abs(self.location[1] - node[1])
            if distFromTurret <= self.attackRange:
                self.attackSquares.append(node)
        print(f'Turret {self.name} : {self.attackSquares}')


def drawGame(grid, turretTracker, alienTracker) -> list:
    gridList = [[f'..{x}..' for x in y] for y in grid]
    for alien in alienTracker:
        gridList[alien.gridLocation[0]][alien.gridLocation[1]] = alien
    for turret in turretTracker:
        gridList[turret.location[0]][turret.location[1]] = f'{turret.name}:{turret.attackRange}:{turret.ammo}'
    for y in gridList:
        temp = []
        for x in y:
            temp.append(x.__str__())
        print(temp)
    return gridList


def findAlienPath(grid, alienPath):
    for searchPos in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        searchSquare = (alienPath[-1][0] + searchPos[0], alienPath[-1][1] + searchPos[1])
        if 0 <= searchSquare[0] < len(grid) and 0 <= searchSquare[1] < len(grid[0]):
            if grid[searchSquare[0]][searchSquare[1]] == '1' and searchSquare not in alienPath:
                alienPath.append(searchSquare)
                return findAlienPath(grid, alienPath)
    return alienPath


def init(grid, turrets):
    origin = None
    alienPath, turretTracker = [], []
    for yIdx, y in enumerate(grid):
        for xIdx, x in enumerate(y):
            if x == '0':
                origin = (yIdx, xIdx)
            elif re.search(r'[A-Z]', x):  # Must be a turret
                turretTracker.append(Turret(x, (yIdx, xIdx), turrets[x][0], turrets[x][1]))

    alienPath = [origin]
    alienPath = findAlienPath(grid, alienPath)
    return alienPath, turretTracker


def fireTurrets(turrets, alienTracker, grid, attack=True):  # Turrets arent getting a chance to attack
    while attack:
        attack = False
        for turret in turrets:
            if turret.ammo > 0:
                for attackSquare in turret.attackSquares:
                    if isinstance(grid[attackSquare[0]][attackSquare[1]], Alien):
                        alien = grid[attackSquare[0]][attackSquare[1]]
                        alien.health -= 1
                        turret.ammo -= 1
                        attack = True
                        print(f'Alien at {alien.gridLocation} in range of turret {turret.name}. '
                              f'Alien {alien.alienID} Attacked! Health: {alien.health} ')
                        if alien.health <= 0:
                            print(f'Alien {alien.alienID} defeated!')
                            grid[attackSquare[0]][attackSquare[1]] = '1'
                            alienTracker.pop(alienTracker.index(alien))
                        break
    print("Turrets out of ammo or no enemy in range")
    for turret in turrets:
        turret.reload()
    return


def tower_defense(_grid, turrets, aliens):
    print(_grid)
    print(turrets)
    print(aliens)
    """ Initiate game"""
    alienID = 0
    alienTracker, spawn = [], True
    alienScore, survivingAliens = 0, []  # Surviving aliens = [wave, health]
    alienPath, turretTracker = init(_grid, turrets)  # Find alienPath(Verified) and turrets
    for turret in turretTracker:  # Determine which squares a turret can attack - Verified Correct
        turret.defineAttackSquares(alienPath)
    alienPath.append('x')  # x indicates end of alien path
    alienGen = (Alien(alien) for alien in aliens)  # Generator for aliens(Verified)

    """Main Game Loop"""
    while True:  # Main Game Loop
        if spawn:  # Spawn alien onto origin
            try:
                newAlien = next(alienGen)
                if newAlien.health > 0:
                    newAlien.setID(alienID)
                    newAlien.setOrigin(alienPath[0])
                    alienID += 1
                    alienTracker.append(newAlien)
            except StopIteration:
                spawn = False
        print('Aliens under fire!')
        grid = drawGame(_grid, turretTracker, alienTracker)
        fireTurrets(turretTracker, alienTracker, grid)
        print('Aliens taking 1 step')
        alienToRemove = False
        for alien in alienTracker:  # Step aliens on grid by 1
            alien.position += 1
            if alienPath[alien.position] == 'x':  # If alien is at end of alien path
                print(f'Alien {alien.alienID} as breached the base!')
                alienScore += alien.health
                survivingAliens.append([alien.alienID, alien.health])
                alienToRemove = alien
            else:
                alien.gridLocation = alienPath[alien.position]  # Update alien grid location
        if alienToRemove: alienTracker.pop(alienTracker.index(alienToRemove))

        # grid = drawGame(_grid, turretTracker, alienTracker)
        # fireTurrets(turretTracker, alienTracker, grid)
        drawGame(_grid, turretTracker, alienTracker)
        if len(alienTracker) == 0 and not spawn:  # No more aliens, end game
            break
    print(survivingAliens)
    return alienScore


grid1 = [
    '0111111',
    '  A  B1',
    ' 111111',
    ' 1     ',
    ' 1C1111',
    ' 111 D1',
    '      1']
turrets1 = {'A': [3, 2], 'B': [1, 4], 'C': [2, 2], 'D': [1, 3]}
aliens1 = [30, 14, 27, 21, 13, 0, 15, 17, 0, 18, 26]

grid2 = ['011  1111',
         ' A1  1BC1',
         ' 11  1 11',
         ' 1D  1 1E',
         ' 111 1F11',
         '  G1 1  1',
         ' 111 1 11',
         ' 1H  1 1I',
         ' 11111 11']
turrets2 = {'A': [1, 4], 'B': [2, 2], 'C': [1, 3], 'D': [1, 3], 'E': [1, 2], 'F': [3, 3], 'G': [1, 2], 'H': [2, 3],
            'I': [2, 3]}
aliens2 = [36, 33, 46, 35, 44, 27, 25, 48, 39, 0, 39, 36, 55, 22, 26]
# aliens2 = [0, 33, 46, 35, 44, 27, 25, 48, 39, 0, 39, 36, 55, 22, 26]
print(Back.RED + '''==============================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
==================================================================================================================
===================================================================+===============================================
==================================================================================================================
==================================================================================================================''')

tic = time.perf_counter()
enemyScore = tower_defense(grid2, turrets2, aliens2)
print(f'EnemyScore: {enemyScore}')
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

# Turret Data: D : Attack Squares: [(5, 6), (4, 5)]


# Turret A : [(2, 1), (1, 2), (0, 1)]
# Turret B : [(2, 7), (1, 8), (0, 7), (0, 6), (0, 5), (1, 5), (2, 5)]
# Turret C : [(2, 7), (1, 8), (0, 7)]
# Turret D : [(4, 2), (3, 1), (2, 2)]
# Turret E : [(4, 8), (3, 7), (2, 8)]
# Turret F : [(6, 7), (5, 8), (4, 8), (4, 7), (3, 7), (2, 7), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (4, 3)]
# Turret G : [(6, 2), (5, 3), (4, 2)]
# Turret H : [(8, 3), (8, 2), (8, 1), (7, 1), (6, 1), (6, 2), (6, 3)]
# Turret I : [(8, 8), (8, 7), (7, 7), (6, 7), (6, 8), (5, 8)]
