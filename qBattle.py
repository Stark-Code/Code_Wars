import logging
import copy
from colorama import init, Back

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format=' - %(message)s')


def printArmy(army):
    logging.info(f'Army {army.armyName}')
    logging.info(army.__str__())
    print("     " * army.turn + "    ^")
    logging.info(army.incomingDamage)
    print('')

# logging.disable(logging.CRITICAL)


class Army:

    def __init__(self, army, distance):
        self.soldiers = list(army)
        self.turn = 0
        self.incomingDamage = {}
        self.distance = distance
        self.armyName = None
        self.lastTurn = None

    def __str__(self):
        return self.soldiers

    def rotateRanks(self):
        if self.turn < len(self.soldiers) - 1:  # 3
            self.turn += 1
        else:
            self.turn = 0
        if self.soldiers[self.turn] == 'x': self.rotateRanks()

    def fireRifle(self) -> int:
        print(f'Army {self.armyName}')
        if self.soldiers[self.turn] == "b":
            logging.info(f'Soldier at position {self.turn} is dying and unable to fire his rifle. (speed: 0)')
            self.soldiers[self.turn] = 'x'
            return 0
        else:
            logging.info(f'Soldier at position {self.turn} has fired his rifle (speed: {self.soldiers[self.turn]})')
            return self.soldiers[self.turn]  # This is the soldier who will fire, return bullet speed

    def updateBulletPositions(self):
        for bullet in self.incomingDamage:
            for distanceIdx in range(len(self.incomingDamage[bullet])):
                if self.incomingDamage[bullet][distanceIdx] <= 0: continue
                self.incomingDamage[bullet][distanceIdx] -= bullet
                if self.incomingDamage[bullet][distanceIdx] <= 0:
                    logging.info(f"Soldier {self.turn} from Army {self.armyName} has been shot!")
                    self.soldiers[self.turn] = 'b'  # Soldier is bleeding out and will die on next rotation

    def trackIncomingBullet(self, bulletSpeed):
        if bulletSpeed == 0: return
        if bulletSpeed in self.incomingDamage:
            self.incomingDamage[bulletSpeed].append(self.distance)
        else:
            self.incomingDamage[bulletSpeed] = [self.distance]


class FieldMarshall:
    def __init__(self, dist, armies):
        self.dist = dist  # Distance between armies
        self.battleField = []
        self.armies = armies
        self.battleWon = False

    def prepareWar(self):
        for armyIdx, army in enumerate(self.armies):
            self.battleField.append(Army(army, self.dist))
            self.battleField[-1].armyName = armyIdx

    def inspectBattleField(self):
        logging.info('\n ...Casualties')
        standingArmies = []
        for army in self.battleField:
            printArmy(army)
            if army.soldiers.count('x') + army.soldiers.count('b') == len(army.soldiers):  # Remove incoming bullets
                logging.info("An army has been defeated!")  # from battlefield
                for _army in self.battleField:
                    _army.incomingDamage = {}
            else:
                standingArmies.append(army)
        self.battleField = standingArmies

        if len(self.battleField) <= 1:
            standingSoldiers = []
            logging.info("The Battle is Over!")
            self.battleField[0].rotateRanks()
            logging.info(f'The winner: {self.battleField[0].armyName}, Leader: {self.battleField[0].turn}')
            print(f'Last turn: {self.battleField[0].turn}')
            print(f'Turn: {self.battleField[0].turn}')
            for soldierIdx in range(self.battleField[0].turn, len(self.battleField[0].soldiers)):
                if self.battleField[0].soldiers[soldierIdx] != 'x':
                    standingSoldiers.append(soldierIdx)
            for soldierIdx in range(0, self.battleField[0].turn):
                if self.battleField[0].soldiers[soldierIdx] != 'x':
                    standingSoldiers.append(soldierIdx)
            return True, self.battleField[0].armyName, tuple(standingSoldiers)
        return False, [], []

    def attack(self):  # Army attacks, Army ranks change, bullet added to enemy table, bullet position updated
        logging.info("The Field Marshall has ordered the troops to fire!")
        for armyIdx, army in enumerate(self.battleField):  # Army is offensive, ArmyIdx+1 Defensive
            if armyIdx == len(self.battleField) - 1:
                armyUnderAttack = self.battleField[0]
            else:
                armyUnderAttack = self.battleField[armyIdx + 1]
            armyUnderAttack.trackIncomingBullet(army.fireRifle())


def queue_battle(dist, *armies):
    FM = FieldMarshall(dist, armies)
    FM.prepareWar()
    FM.inspectBattleField()

    while not FM.battleWon:
        FM.attack()
        for army in FM.battleField:
            logging.info('Troops Rotating')
            army.rotateRanks()
            printArmy(army)
            army.updateBulletPositions()
        FM.battleWon, winningArmy, standingSoldiers = FM.inspectBattleField()

    print(f'Winning Army: {winningArmy}')
    print(f'Standing Soldiers: {standingSoldiers}')
    return winningArmy, standingSoldiers


test = (
    (100, (25, 38, 55, 46, 82), (64, 90, 37, 25, 58)),
    (200, (61, 83, 37, 55, 92, 35, 68, 72), (90, 81, 36, 114, 67, 25, 31, 84)),
    (300, (98, 112, 121, 95, 63), (120, 94, 90, 88, 30), (116, 144, 45, 200, 32)),
    (400, (186, 78, 56, 67, 78, 127, 78, 192), (78, 67, 208, 45, 134, 212, 82, 99),
     (327, 160, 49, 246, 109, 98, 44, 57)),
    (500, (345, 168, 122, 269, 151), (56, 189, 404, 129, 101), (364, 129, 209, 163, 379), (520, 224, 154, 74, 420)),)

# sols = (
# 	(1,(3,2)),
# 	(0,(6,7)),
# 	(0,(2,)),
# 	(2,(0,2,5)),
# 	(-1,()),
# )

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

# result = queue_battle(100, (25, 38, 55, 46, 82), (64, 90, 37, 25, 58))
# result = queue_battle(200, (61, 83, 37, 55, 92, 35, 68, 72), (90, 81, 36, 114, 67, 25, 31, 84))
result = queue_battle(300, (98, 112, 121, 95, 63), (120, 94, 90, 88, 30), (116, 144, 45, 200, 32))
# result = queue_battle(400, (186, 78, 56, 67, 78, 127, 78, 192), (78, 67, 208, 45, 134, 212, 82, 99),
                      # (327, 160, 49, 246, 109, 98, 44, 57))
# result = queue_battle(500, (345, 168, 122, 269, 151), (56, 189, 404, 129, 101), (364, 129, 209, 163, 379), (520, 224, 154, 74, 420))
print(result)
'''
Soldiers Fire
Bullets Added to incoming damage table
Soldiers rotate
Bullet Positions Updated
Check for deaths
Soldiers Fire
'''
# I think a soldier fires, line rotates, then the soldier at the front of the line gets hit. He shouldnt be able
# to attack, but the algorithm searches for the next living soldier.
