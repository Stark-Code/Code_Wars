import time
import os
merchants = {}
enemies = {}
demonLord = {}

class Player:

    def __init__(self, health, attack, defense, experience, bag, posData: []):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.experience = experience
        self.bag = bag
        self.location = posData[1]
        self.orientation = posData[0]

    def getHealth(self):
        return self.health

    def setHealth(self):
        self.health = 3
        print(f"Player Health Increased to {self.health}!")
        self.bag.remove("H")

    def takeDamage(self, enemyID, attackingEnemies):
        if enemyID == "E":
            damage = 2
        elif enemyID == "D":
            damage = 3
        for i in range(attackingEnemies):
            self.health -= max(0, (damage - self.defense))
            print(f"Player suffered {max(0, (damage - self.defense))} damage!")
            print(f"Current Health {self.health}")
            if self.health <= 0:
                print("You Died!")
                return True

    def getAttack(self):
        return self.attack

    def setAttack(self):
        self.attack += 1
        print(f"Player Attack Increased to {self.attack}!")

    def getExperience(self):
        if self.experience == 3:
            print("Player Leveled!")
            self.setAttack()
            self.experience = 0

    def setExperience(self):
        self.experience += 1
        self.getExperience()

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def getOrientation(self):
        return self.orientation

    def setOrientation(self, orientation):
        self.orientation = orientation

    def getDefense(self):
        return self.defense

    def setDefense(self):
        self.defense += 1
        print(f"Player Defense Increased to {self.defense}!")

    def addItem(self, itemName):
        self.bag.append(itemName)
        print(f"1 {itemName} added to inventory!")
        self.bag.sort()
        print(f"Current Inventory: {self.bag}")

    def useItem(self, itemName, argMap):
        if itemName == "H":
            if self.bag.count("H") > 0 and self.health < 3:
                self.setHealth()
                print("Health Potion Used!")
                return False, argMap
            else:
                return True, argMap
        if itemName == "C":
            if self.bag.count("C") > 0:
                print("Attempting to use Coin")
                return checkCoinLegality(self, argMap)
            else:
                print("No coins!")
                return True, argMap  # gameOver
        if itemName == "K":
            if self.bag.count("K") > 0:
                print("Key Used")
                return checkKeyLegality(self, argMap)
            else:
                print("No Keys!")
                return True, argMap

    def removeItem(self, itemName):
        self.bag.remove(itemName)
        print(f"{itemName} removed from inventory!")
        print(self.getInventory())

    def getInventory(self):
        return self.bag


def getPlayerDirectionAndLocation(argMap):
    playerPos = -1
    for x in range(len(argMap)):
        if argMap[x].count("<") > 0:
            playerPos = argMap[x].index("<")
        if argMap[x].count("^") > 0:
            playerPos = argMap[x].index("^")
        if argMap[x].count("v") > 0:
            playerPos = argMap[x].index("v")
        if argMap[x].count(">") > 0:
            playerPos = argMap[x].index(">")
        if playerPos > -1:
            return argMap[x][playerPos], [x, playerPos]


def checkCoinLegality(argPlayer, argMap):
    orientation = argPlayer.getOrientation()
    playerLoc = argPlayer.getLocation()
    if orientation == "^":
        checkPos = [playerLoc[0] - 1, playerLoc[1]]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a coin here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "M":
            print("Merchant Not Found!")
            return True, argMap
        argPlayer.removeItem("C")
        merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] += 1
        if merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] == 3:
            argMap[checkPos[0]][checkPos[1]] = " "
            print("Merchant has left!")
        print(merchants)
        return False, argMap
    if orientation == ">":
        checkPos = [playerLoc[0], playerLoc[1] + 1]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a coin here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "M":
            print("Merchant Not Found!")
            return True, argMap
        argPlayer.removeItem("C")
        merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] += 1
        if merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] == 3:
            argMap[checkPos[0]][checkPos[1]] = " "
            print("Merchant has left!")
        return False, argMap
    if orientation == "v":
        checkPos = [playerLoc[0] + 1, playerLoc[1]]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a coin here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "M":
            print("Merchant Not Found!")
            return True, argMap
        argPlayer.removeItem("C")
        merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] += 1
        if merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] == 3:
            argMap[checkPos[0]][checkPos[1]] = " "
            print("Merchant has left!")
        return False, argMap
    if orientation == "<":
        checkPos = [playerLoc[0], playerLoc[1] - 1]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a coin here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "M":
            print("Merchant Not Found!")
            return True, argMap
        argPlayer.removeItem("C")
        merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] += 1
        if merchants[f"Merchant{checkPos[0]}{checkPos[1]}"] == 3:
            argMap[checkPos[0]][checkPos[1]] = " "
            print("Merchant has left!")
        return False, argMap


def checkKeyLegality(argPlayer, argMap):
    orientation = argPlayer.getOrientation()
    playerLoc = argPlayer.getLocation()
    if orientation == "^":
        checkPos = [playerLoc[0] - 1, playerLoc[1]]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a key here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "-":
            print("No door found!")
            return True, argMap
        argPlayer.removeItem("K")
        argMap[checkPos[0]][checkPos[1]] = " "
        return False, argMap
    if orientation == ">":
        checkPos = [playerLoc[0], playerLoc[1] + 1]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a key here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "|":
            print("No door found!")
            return True, argMap
        argPlayer.removeItem("K")
        argMap[checkPos[0]][checkPos[1]] = " "
        return False, argMap
    if orientation == "v":
        checkPos = [playerLoc[0] + 1, playerLoc[1]]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a key here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "-":
            print("No door found!")
            return True, argMap
        argPlayer.removeItem("K")
        argMap[checkPos[0]][checkPos[1]] = " "
        return False, argMap
    if orientation == "<":
        checkPos = [playerLoc[0], playerLoc[1] - 1]
        gameOver = checkGameOver(" ", checkPos, argMap)
        if gameOver:
            print("You cant use a key here!")
            return True, argMap
        if argMap[checkPos[0]][checkPos[1]] != "|":
            print("No door found!")
            return True, argMap
        argPlayer.removeItem("K")
        argMap[checkPos[0]][checkPos[1]] = " "
        return False, argMap


def updateMap(prevLoc, player, argMap):
    print("Updating Map")
    currPlayerLoc = player.getLocation()
    orientation = player.getOrientation()
    argMap[prevLoc[0]][prevLoc[1]] = " "
    argMap[currPlayerLoc[0]][currPlayerLoc[1]] = orientation
    for x in argMap:
        print(x)
    return argMap


def checkGameOver(argNextStep, argNextLoc, argMap):
    if argNextLoc[0] < 0 or argNextLoc[0] >= len(argMap):  # y
        return True
    if argNextLoc[1] < 0 or argNextLoc[1] >= len(argMap[argNextLoc[0]]):  # x
        return True
    if argNextStep not in [" ", "C", "K", "X", "S", "H"]:
        print("You cant do that!")
        return True  # GameOver


def checkNextPosition(argPlayer):
    currOrient = argPlayer.getOrientation()
    currLoc = argPlayer.getLocation()
    movementDelta = [0, 0]
    if currOrient == "<":
        movementDelta = [0, -1]
    if currOrient == ">":
        movementDelta = [0, 1]
    if currOrient == "^":
        movementDelta = [-1, 0]
    if currOrient == "v":
        movementDelta = [1, 0]
    y = currLoc[0] + movementDelta[0]  # Player wants to move to this position
    x = currLoc[1] + movementDelta[1]  # Player wants to move to this position
    return y, x


def moveForward(argPlayer, argMap):  # currDir, currLoc

    prevLoc = argPlayer.getLocation().copy()
    y, x = checkNextPosition(argPlayer)
    argPlayer.setLocation([y, x])
    print(f"Player wants to move forward to: {[y, x]}")
    if checkGameOver(" ", [y, x], argMap):
        return True, argMap
    nextStep = argMap[y][x]
    if checkGameOver(nextStep, [y, x], argMap):
        return True, argMap
    if nextStep == "C":  # Coin Changed from elif to if
        argPlayer.addItem("C")
    elif nextStep == "H":  # Health Potion
        argPlayer.addItem("H")
    elif nextStep == "K":  # Key
        argPlayer.addItem("K")
    elif nextStep == "S":  # Shield
        argPlayer.setDefense()
    elif nextStep == "X":  # Sword
        argPlayer.setAttack()
    return False, updateMap(prevLoc, argPlayer, argMap)


def checkForEnemies(playerLoc, argMap):
    enemiesFound = 0
    demonLordsFound = 0
    if playerLoc[1] + 1 < len(argMap[0]):
        if argMap[playerLoc[0]][playerLoc[1] + 1] == "E":  # Check Right
            print("Enemy found to the East!")
            enemiesFound += 1
        if argMap[playerLoc[0]][playerLoc[1] + 1] == "D":
            print("Demon Lord found to the East!")
            demonLordsFound += 1
    if playerLoc[1] - 1 >= 0:
        if argMap[playerLoc[0]][playerLoc[1] - 1] == "E":  # Check Left
            print("Enemy found to the West!")
            enemiesFound += 1
        if argMap[playerLoc[0]][playerLoc[1] - 1] == "D":
            print("Demon Lord found to the West!")
            demonLordsFound += 1
    if playerLoc[0] + 1 < len(argMap):
        if argMap[playerLoc[0] + 1][playerLoc[1]] == "E":  # Check Down
            print("Enemy found to the South!")
            enemiesFound += 1
        if argMap[playerLoc[0] + 1][playerLoc[1]] == "D":
            print("Demon Lord found to the South!")
            demonLordsFound += 1
    if playerLoc[0] - 1 >= 0:
        if argMap[playerLoc[0] - 1][playerLoc[1]] == "E":  # Check Up
            print("Enemy found to the North!")
            enemiesFound += 1
        if argMap[playerLoc[0] - 1][playerLoc[1]] == "D":
            print("Demon Lord found to the North!")
            demonLordsFound += 1
    print(enemiesFound)
    return enemiesFound, demonLordsFound


def attack(argPlayer, argMap):
    y, x = checkNextPosition(argPlayer)  # Position player wants to attack
    if argMap[y][x] == "E":
        enemies[f"Enemy{y}{x}"] -= argPlayer.getAttack()
        if enemies[f"Enemy{y}{x}"] <= 0:
            print("Enemy Defeated!")
            argPlayer.setExperience()
            return "Enemy Dead", [y, x]
        else:
            print(f"Enemy Damaged! Enemy Health: {enemies[f'Enemy{y}{x}']}")
            return "Enemy Alive", [y, x]
    elif argMap[y][x] == "D":
        demonLord["DemonLord"] -= argPlayer.getAttack()
        if demonLord["DemonLord"] <= 0:
            print("DemonLord Defeated!")
            argPlayer.setExperience()
            return "Enemy Dead", [y, x]
        else:
            print(f"DemonLord Damaged! Demon Lord Health: {demonLord['DemonLord']}")
            return "DemonLord Alive", [y, x]
    else:
        print("You cant attack that!")
        return "Enemy Not Found", argMap


def parseActions(action, argMap, argPlayer):
    playerLoc = argPlayer.getLocation()
    enemiesFound, demonLordsFound = checkForEnemies(playerLoc, argMap)
    if action == "F":
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        return moveForward(argPlayer, argMap)
    elif action == "^":
        argPlayer.setOrientation("^")
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        return False, updateMap(playerLoc, argPlayer, argMap)
    elif action == ">":
        argPlayer.setOrientation(">")
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        return False, updateMap(playerLoc, argPlayer, argMap)
    elif action == "v":
        argPlayer.setOrientation("v")
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        return False, updateMap(playerLoc, argPlayer, argMap)
    elif action == "<":
        argPlayer.setOrientation("<")
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        return False, updateMap(playerLoc, argPlayer, argMap)
    elif action == "A":
        enemyStatus, enemyPos = attack(argPlayer, argMap)
        if enemyStatus == "Enemy Not Found":  # Player trying to attack empty space
            return True, argMap
        if enemyStatus == "Enemy Alive":
            gameOver = argPlayer.takeDamage("E", enemiesFound)
            if gameOver:
                return True, argMap
            else:
                return False, argMap
        if enemyStatus == "DemonLord Alive":
            gameOver = argPlayer.takeDamage("D", 1)
            if gameOver:
                return True, argMap
            else:
                return False, argMap
        if enemyStatus == "Enemy Dead":
            argMap[enemyPos[0]][enemyPos[1]] = " "
            return False, argMap
    elif action == "C" or action == "K":
        return argPlayer.useItem(action, argMap)
    elif action == "H":  # If player survives attack, returns the state of game
        gameState = argPlayer.useItem(action, argMap)
        gameOver = argPlayer.takeDamage("E", enemiesFound)
        gameOver2 = argPlayer.takeDamage("D", demonLordsFound)
        if gameOver or gameOver2:
            return True, argMap
        else:
            return gameState


def rpg(field, action):
    gameOver = False

    #  Create Player
    player = Player(3, 1, 1, 0, [], getPlayerDirectionAndLocation(field))

    # Find Merchants
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == "M":
                merchants.update({f"Merchant{y}{x}": 0})

    # Find Enemies
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == "E":
                enemies.update({f"Enemy{y}{x}": 1})
    print(f"Enemy Table: {enemies}")
    demonLord.update({"DemonLord": 10})

    playerOrientation, playerLocation = getPlayerDirectionAndLocation(field)
    player.setLocation(playerLocation)
    player.setOrientation(playerOrientation)
    gameOver, field = parseActions(action, field, player)

    if gameOver:
        print("GameOver!")
        return None
    else:
        return field, player.getHealth(), player.getAttack(), player.getDefense(), player.getInventory()


actionsList = "^FFvFF<FFFFFAFA>F^F<FA^F<FF>FFF^FF<CCCFFF>FFFFFKFAFF<FFFvFFFF<FFFFAAHAA"
m = [['S', 'H', 'M', ' ', ' ', ' ', '|', 'E', 'X'],
     ['#', '#', '#', ' ', ' ', ' ', '#', '#', '#'],
     ['C', 'C', 'K', ' ', ' ', ' ', ' ', ' ', 'C'],
     [' ', 'E', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['D', 'E', 'E', ' ', ' ', ' ', ' ', ' ', '^']]


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


result = [m]
for inputs in actionsList:
    result = rpg(result[0], inputs)
    cls()
    for x in result[0]:
        print(x)
    time.sleep(.5)

