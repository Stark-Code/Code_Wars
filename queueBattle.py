def resetBullets(armies):
    print("All bullets removed from field")
    print(f"Armies: {armies}")
    incomingDamage = {}
    for idx in range(len(armies)):
        name = "Army_" + str(idx)
        incomingDamage[name] = {}
    return incomingDamage


def decodeArmy(encodedRank):
    decodedRank = encodedRank.split("-")
    return int(decodedRank[0])


def findEnemy(armies):
    # Army : Enemy
    myEnemy = {}
    for idx in range(len(armies)):
        myEnemy[idx] = idx + 1
        if idx == len(armies) - 1:
            myEnemy[idx] = 0
    print(f"myEnemy Table (Army : Enemy): {myEnemy}")
    return myEnemy


def changeRank(armies, incomingDamage, myEnemy):
    if len(armies) > 1:
        for army in armies:  # Rotate lines
            frontSoldier = army[0]  # Might cause problems?
            army.pop(0)
            army.append(frontSoldier)
            if army[-1] == 0:
                army.pop(-1)
            elif decodeArmy(army[-1]) == 0:  # Soldier elimination
                army.pop(-1)
        print(f"Armies have changed rank!: {armies}")
        survivingArmies = []
        reset = False
        for army in armies:
            if len(army) > 0:
                survivingArmies.append(army)
            else:
                reset = True
        if reset:
            incomingDamage = resetBullets(survivingArmies)
            myEnemy = findEnemy(survivingArmies)
        return survivingArmies, incomingDamage, myEnemy


def checkBulletLocations(armies, incomingDamage):  # incomingDamage = {'Army_X' : {bulletSpeed: distanceLeft}, ...

    print("Updating bullet locations")
    print(f"Army Value: {armies}")
    for army in incomingDamage:
        for bulletSpeed in incomingDamage[army]:  # Bullet Speed : Distance
            activeBullets = []
            for idx in range(len(incomingDamage[army][bulletSpeed])):
                incomingDamage[army][bulletSpeed][idx] -= bulletSpeed
                if incomingDamage[army][bulletSpeed][idx] <= 0:
                    armies[int(army[-1])][0] = 0  # Setting soldier to 0
                else:
                    activeBullets.append(incomingDamage[army][bulletSpeed][idx])
            incomingDamage[army][bulletSpeed] = activeBullets


def shootBullet(armies, myEnemy, incomingDamage, dist):
    print(f"Armies&&& {armies}")
    for army in myEnemy:  # {0: 1, 1: 0}
        key = "Army_" + str(myEnemy[army])
        print(f"This {armies[army][0]}")
        if armies[army][0] != 0:
            decodedSoldier = decodeArmy(armies[army][0])
        else:
            decodedSoldier = 0
        if decodedSoldier != 0:
            if decodedSoldier in incomingDamage[key]:
                incomingDamage[key][decodedSoldier].append(dist)
            else:
                incomingDamage[key][decodedSoldier] = [dist]
    print(f"Shot added to damage table {incomingDamage}")


def queue_battle(dist, *args):
    armies = []
    encodedArmies = []
    for arg in args:  # Change Tuple to List
        armies.append(list(arg))

    for idx in range(len(armies)):
        encodedArmies.append([])
        for soldierIdx in range(len(armies[idx])):
            encodedArmies[idx].append(str(armies[idx][soldierIdx]) + "-" + str(idx) + "-" + str(soldierIdx))
    print(encodedArmies)
    print(f"Armies: {armies}")
    print(f"Distance: {dist}")
    incomingDamage = resetBullets(encodedArmies)
    while len(encodedArmies) > 1:
        myEnemy = findEnemy(encodedArmies)
        checkBulletLocations(encodedArmies, incomingDamage)
        shootBullet(encodedArmies, myEnemy, incomingDamage, dist)
        encodedArmies, incomingDamage, myEnemy = changeRank(encodedArmies, incomingDamage, myEnemy)

    flatArmy = [item for sublist in encodedArmies for item in sublist]
    soldierPositions = []
    armyPos = 0

    for x in flatArmy:
        temp = x.split("-")
        armyPos = temp[0]
        soldierPositions.append(temp[-1])


    return (armyPos, tuple(soldierPositions))


# queue_battle(500, (345, 168, 122, 269, 151), (56, 189, 404, 129, 101), (364, 129, 209, 163, 379),
#              (520, 224, 154, 74, 420))
l = queue_battle(100, (25, 38, 55, 46, 82), (64, 90, 37, 25, 58))
# r = queue_battle(100, (25, 38, 55, 46, 82), (64, 90, 37, 25, 58), (38, 60, 87, 95, 55), (94, 91, 73, 65, 88))

# m = queue_battle(100, (25, 38, 55, 46, 82), (60, 50, 70, 50, 50))



# Bullet speeds are rewriting themselves in damage table




#     for idx, soldier in enumerate(army):
        #         if idx < len(army) - 1:
        #             army[idx], army[idx + 1] = army[idx + 1], army[idx]