
numbers = [1, 2]


def buildConstraintsMatrix(cover):
    constraintsMatrix = {}
    for y in range(len(cover)):
        for x in range(len(cover[y])):
            for num in numbers:
                constraintsMatrix[num, y, x] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return constraintsMatrix


#  Number in each row/column
def constraintOne(constraintMatrix, cover):
    idx = 0
    for y in range(len(cover)):
        for x in range(len(cover)):
            for num in numbers:
                constraintMatrix[num, y, x][idx] = 1
            idx += 1
    return constraintMatrix


#  Number in each row
def constraintTwo(constraintMatrix, cover):
    constraints = len(cover[0]) * len(cover)  # Number of constraints for type 2
    for y in range(len(cover)):
        idx = len(numbers) * y + constraints
        for x in range(len(cover[y])):
            idx -= len(numbers) * x
            for num in numbers:
                constraintMatrix[num, y, x][idx] = 1
                idx += 1

    return constraintMatrix


def constraintThree(constraintMatrix, cover):
    constraints = 2 * (len(cover[0]) * len(cover))  # Number of constraints for type 3
    for y in range(len(cover)):
        idx = constraints
        for x in range(len(cover[y])):
            for num in numbers:
                print(f"Idx: {idx}")
                constraintMatrix[num, y, x][idx] = 1
                idx += 1

    return constraintMatrix

def constraintFour(constraintMatrix, cover):
    constraints = 3 * #bL
    for y in range(len(cover)):
        constraints = 3 *  # bL
        for x in range(len(cover[y])):
            for num in number:
                constraintMatrix[num, y, x] = 1

# Fill (row1 col1), (row1, col2), (row1, col3), (row1, col4) >> (row1, col9)

