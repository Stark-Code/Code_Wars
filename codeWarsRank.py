class User:
    def __init__(self):
        self.rank = -8
        self.progress = 0
        self.ranks = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]

    def calculateProgress(self, grade):
        gradeIdx, rankIdx = self.ranks.index(grade), self.ranks.index(self.rank)
        if self.rank < 8:
            if grade == self.rank: return 3
            elif rankIdx - gradeIdx == 1: return 1
            elif rankIdx - gradeIdx > 1: return 0
            else:
                d = abs(gradeIdx - rankIdx)
                return 10 * d * d
        return 0

    def inc_progress(self, grade):
        if grade not in self.ranks: raise ValueError
        if self.rank < 8:
            _progress = self.calculateProgress(grade)
            self.progress += _progress
        else: return

        def applyProgress(progress):
            if self.rank == 8:
                self.progress = 0
                return
            if self.progress >= 100:
                self.progress -= 100
                if self.rank < 8:
                    self.rank = self.ranks[self.ranks.index(self.rank) + 1]
                if self.rank == 8: self.progress = 0
            if self.progress >= 100:
                return applyProgress(self.progress)
        applyProgress(_progress)

user = User()
print(user.rank) # => -8
print(user.progress) # => 0
user.inc_progress(-4)
print(user.progress) # => 10
user.inc_progress(-5) # will add 90 progress
print(user.progress) # => 0 # progress is now zero
print(user.rank)