import border
import time
import sys


class Blox:
    def __init__(self, location):
        self.location = location
        self.orientation = 'upRight'

    @property
    def setOrientation(self):
        return self.orientation

    def setLocation(self, location):
        return self.location


def printGrid(grid):
    for row in grid:
        temp = []
        for x in row:
            if x == '1':
                temp.append('░')
            elif x == '0':
                temp.append(' ')
            elif x == "B":
                temp.append('█')
            else: temp.append(x)
        print(temp)


def blox_solver(grid):
    printGrid(grid)
    blox = Blox


tests = [
    ['1110000000',
     '1B11110000',
     '1111111110',
     '0111111111',
     '0000011X11',
     '0000001110'],
    ['000000111111100',
     '111100111001100',
     '111111111001111',
     '1B11000000011X1',
     '111100000001111',
     '000000000000111'],
    ['00011111110000',
     '00011111110000',
     '11110000011100',
     '11100000001100',
     '11100000001100',
     '1B100111111111',
     '11100111111111',
     '000001X1001111',
     '00000111001111'],
    ['11111100000',
     '1B111100000',
     '11110111100',
     '11100111110',
     '10000001111',
     '11110000111',
     '11110000111',
     '00110111111',
     '01111111111',
     '0110011X100',
     '01100011100'],
    ['000001111110000',
     '000001001110000',
     '000001001111100',
     'B11111000001111',
     '0000111000011X1',
     '000011100000111',
     '000000100110000',
     '000000111110000',
     '000000111110000',
     '000000011100000']
]
# example_sols = [['RRDRRRD','RDDRRDR','RDRRDDR'],
#                 ['ULDRURRRRUURRRDDDRU','RURRRULDRUURRRDDDRU'],
#                 ['ULURRURRRRRRDRDDDDDRULLLLLLD'],
#                 ['DRURURDDRRDDDLD'],
#                 ['RRRDRDDRDDRULLLUULUUURRRDDLURRDRDDR','RRRDDRDDRDRULLLUULUUURRDRRULDDRRDDR','RRRDRDDRDDRULLLUULUUURRDRRULDDRRDDR','RRRDDRDDRDRULLLUULUUURRRDDLURRDRDDR']]
border.printBorder()
tic = time.perf_counter()
blox_solver(tests[0])
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")

