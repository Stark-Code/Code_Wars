rank = {  # Row
    "8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7
}
file = {  # Col
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7
}


def updateBoard(turn, movement, board):
    print(f"Movement: {movement}")
    if type(movement[0]) is list:  # Attack , movement ; [[attackingPawnPos], [attackedPawnPos]]
        print('Update Board with Attack')
        board[movement[0][0]][movement[0][1]] = "."
        if turn == 1:
            board[movement[1][0]][movement[1][1]] = "P"
        else:
            board[movement[1][0]][movement[1][1]] = "p"
    elif turn == 1:  # Standard Movement
        print("Standard Movement")
        board[movement[0] + 1][movement[1]] = "."
        board[movement[0]][movement[1]] = "P"
    else:
        board[movement[0] - 1][movement[1]] = "."
        board[movement[0]][movement[1]] = "p"
    return board


def checkLegalAttack(turn, attackingPawnPos, attackedPawnPos, board):
    if turn == 1:
        if board[attackingPawnPos[0]][attackingPawnPos[1]] == "P" and \
                board[attackedPawnPos[0]][attackedPawnPos[1]] == "p":
            print("White attacking Black")
            return True
        else:
            print("Attack Not Valid")
            return False
    else:
        if board[attackingPawnPos[0]][attackingPawnPos[1]] == "p" and \
                board[attackedPawnPos[0]][attackedPawnPos[1]] == "P":
            print("Black attacking White")
            return True
        else:
            print("Attack not Valid 2")
            return False


def pawnAttack(turn, movement, board):
    attackedPawnPos = [rank[movement[1][1]], file[movement[1][0]]]
    if turn == 1:
        attackingPawnPos = [rank[movement[1][1]] + 1, file[movement[0][0]]]
    else:
        attackingPawnPos = [rank[movement[1][1]] - 1, file[movement[0][0]]]
    print(f"Attacked Pawn Position: {attackedPawnPos}")
    print(f"Attacking Pawn Position: {attackingPawnPos}")
    print(pawnAttack)
    return checkLegalAttack(turn, attackingPawnPos, attackedPawnPos, board), [attackingPawnPos, attackedPawnPos]


def checkLegalMove(turn, movement, board, move):  # move : String representation of movement
    if turn == 1:  # Check to see if there is a pawn on square behind movement
        if board[movement[0] + 1][movement[1]] == "P" and board[movement[0]][movement[1]] == ".":  # Check White
            return True, board
        elif move[1] == "4":  # Check 2 step movement for 1st move
            if board[movement[0] + 2][movement[1]] == "P" and board[movement[0] + 1][movement[1]] == "." and \
                    board[movement[0]][movement[1]] == ".":  # Check White
                board = updateBoard(turn, [movement[0]+1, movement[1]], board)  # Updating in between move
                return True, board
            else:
                return False, board
        else:
            return False, board
    else:
        if board[movement[0] - 1][movement[1]] == "p" and board[movement[0]][movement[1]] == ".":  # Check Black
            return True, board
        elif move[1] == "5":  # Check 2 step movement for 1st move
            if board[movement[0] - 2][movement[1]] == "p" and board[movement[0] - 1][movement[1]] == "." and \
                    board[movement[0]][movement[1]] == ".":  # Check White
                board = updateBoard(turn, [movement[0]-1, movement[1]], board)  # Updating in between move
                return True, board
            else:
                return False, board
        else:
            return False, board


def pawn_move_tracker(moves):
    board = [
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        [".", ".", ".", ".", ".", ".", ".", "."]
    ]
    turn = 1  # White: 1, Black: 0
    for move in moves:
        if move[1] == "x":  # Attack
            pawnAttackCommand = move.split("x")
            legal, movement = pawnAttack(turn, pawnAttackCommand, board)
        else:  # Move Pawn Forward
            movement = [rank[move[1]], file[move[0]]]  # [y, x]
            legal, board = checkLegalMove(turn, movement, board, move)
        if legal:
            board = updateBoard(turn, movement, board)
        else:
            return f"{move} is invalid"
        turn = 0 if turn else 1
    for row in board:
        print(row)
    return board


# r, b = pawn_move_tracker(["e4", "d5", "e5", "a6", "e6", "a5"])  # , "dxe4"
r =  pawn_move_tracker(['dxe4', "e3", 'd5', 'g4', 'd4', 'exd4'])
print(r)
# for row in b:
#     print(row)
# White Moves First (P)
# Black (p)
