import math

ranks = ["Pushover", "Novice", "Fighter", "Warrior", "Veteran", "Sage", "Elite", "Conqueror", "Champion", "Master",
         "Greatest"]


class Warrior:
    def __init__(self):
        self.experience = 100
        self.achievements = []
        self.rank = ranks[math.floor(self.experience / 100) // 10]
        self.level = math.floor(self.experience / 100)

    def addExp(self, experience):
        if self.experience < 10000:
            self.experience += experience
            if self.experience < 10000: self.experience = 10000

    def battle(self, enemyLevel):
        if 0 <= enemyLevel > 100: return 'Invalid level'
        levelDifference = self.level - enemyLevel
        if levelDifference == 0:
            self.addExp(10)
            return "A good fight"
        elif levelDifference == 1:
            self.addExp(5)
            return "An intense fight"
        elif levelDifference > 1:
            return "Easy fight"
        elif levelDifference < 0:  # Enemy is higher level
            if levelDifference <= -5 and self.level < enemyLevel // 10:
                return "You've been defeated"
            else:
                self.addExp(20 * (levelDifference*levelDifference))
                return "An intense fight"

    def training(self, trainingData):  # 0: Description of fight, 1: Exp gained, 2: Min Level Required
        if self.level >= trainingData[2]:
            self.achievements.append(trainingData[0])
            self.experience += trainingData[1]
            return trainingData[0]
        else: return "Not strong enough"


john = Warrior()
print(john.rank)
print(john.level)
