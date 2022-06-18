def printBoard(field):
    for row in field:
        print(row)


def markAdj(field, location, searchParams):
    for direction in searchParams:
        searchSquare = [location[0] + direction[0], location[1] + direction[1]]
        if 0 <= searchSquare[0] < 10 and 0 <= searchSquare[1] < 10:
            field[searchSquare[0]][searchSquare[1]] = "-"
    return field


def searchDown(field, location, shipLength):
    while location[0] + 1 < len(field) and field[location[0] + 1][location[1]] == 1:
        field[location[0] + 1][location[1]] = "x"
        shipLength += 1
        location[0] += 1
        field = markAdj(field, location, [[0, -1], [0, 1]])  # Mark left and right of ship
    location[0] += 1  # Mark bottom border of ship
    field = markAdj(field, location, [[0, -1], [0, 0], [0, 1]])
    return field, shipLength


def searchRight(field, location, shipLength):
    while location[1] + 1 < len(field[0]) and field[location[0]][location[1] + 1] == 1:
        field[location[0]][location[1] + 1] = "x"
        shipLength += 1
        location[1] += 1
        field = markAdj(field, location, [[-1, 0], [1, 0]])  # Mark top and bottom of ship
    location[1] += 1  # Mark right border of ship
    field = markAdj(field, location, [[-1, 0], [0, 0], [1, 0]])
    return field, shipLength


def recordShip(ships, shipLength):
    print(ships)
    if str(shipLength) in ships:
        if ships.get(str(shipLength)) >= 1:
            ships[str(shipLength)] -= 1
            return ships, False
        else:
            return ships, True
    else:
        return ships, True  # Game Over


def validate_battlefield(field):
    gameOver = False
    ships = {
        "4": 1,  # Battleship
        "3": 2,  # Cruiser
        "2": 3,  # Destroyer
        "1": 4  # Submarine
    }

    for rowIdx in range(len(field)):
        for colIdx in range(len(field[rowIdx])):
            if field[rowIdx][colIdx] == 1 and not gameOver:
                print(f'Ship found at {rowIdx, colIdx}')
                field[rowIdx][colIdx] = "x"
                field = markAdj(field, [rowIdx, colIdx], [[0, -1], [-1, -1], [-1, 0]])
                field, shipLength = searchDown(field, [rowIdx, colIdx], shipLength=1)
                if shipLength == 1:
                    field, shipLength = searchRight(field, [rowIdx, colIdx], shipLength)
                print(f'Ship found: {shipLength}')
                ships, gameOver = recordShip(ships, shipLength)
                printBoard(field)
    print(ships)
    #  Confirm Board is Valid
    if gameOver:
        return False
    for key in ships:
        if ships[key] != 0:
            return False
    return True


battleField = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
               [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

r = validate_battlefield(battleField)
print(r)
# 1 - 4 size Battleship
# 2 - 3 size Cruiser
# 3 2 size Destroyer
# 4 1 size Submarine

# Search Left to Right, Up to Down
# Find a marker - Search Right - Find a marker - Search Right Else - Search Down.
# Track which ship is found, along with head and tail of ship
# Get orientation of ship. Make sure no other ships are touching it.
