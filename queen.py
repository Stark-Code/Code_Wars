import copy
import sys


def translateCoordinate(board, initPos):
    result = ""
    y = [str(y) for y in range(1, len(board)+1)]
    y.reverse()
    if y[0] == "10":
        y[0] = "0"
    x = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
    if initPos:
        return [y.index(initPos[1]), x.index(initPos[0])]
    else:
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "Q":
                    result += f"{x[col] + y[row]},"
    return result[:-1]


def checkAttackSquares(queenPos, board):
    movements = []
    up, down = [-1, 0], [1, 0]
    left, right = [0, -1], [0, 1]
    upLeft, upRight = [-1, -1], [-1, 1]
    downLeft, downRight = [1, -1], [1, 1]
    movements.extend((up, down, left, right, upLeft, upRight, downLeft, downRight))
    for moves in movements:
        lookAhead = [queenPos[0], queenPos[1]]
        while True:
            lookAhead[0] += moves[0]
            lookAhead[1] += moves[1]
            if -1 < lookAhead[0] < len(board) and -1 < lookAhead[1] < len(board[0]):
                board[lookAhead[0]][lookAhead[1]] = "x"
            else:
                break
    return board


def findEmptyRow(board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == ".":
                return y
    return None


def search(board, queenCount):
    if queenCount == len(board):
        return True, copy.deepcopy(board) # solutionFound, solution

    emptyRow = findEmptyRow(board)
    if emptyRow is None:
        return False, []

    for idx, item in enumerate(board[emptyRow]):
        if item == ".":
            board[emptyRow][idx] = "Q"
            queenCount += 1
            updatedBoard = checkAttackSquares([emptyRow, idx], copy.deepcopy(board))
            for row in updatedBoard:
                print(row)
            print(f"queen count: {queenCount}")
            solutionFound, solution = search(updatedBoard, queenCount)
            if solutionFound:
                print("Solution Found!")
                return solutionFound, solution
            else:
                board[emptyRow][idx] = "."
                queenCount -= 1
                for row in board:
                    print(row)
                print(" ")
    print("Backtracking")
    return False, solution


def queens(position, size):
    board = [["." for _ in range(size)] for _ in range(size)]  # Initialize board
    initPos = translateCoordinate(board, position)  # Encode 'c6' >> [0, 2]
    board[initPos[0]][initPos[1]] = "Q"  # Set initial queen position
    board = checkAttackSquares(initPos, board)  # Set initial attacked squares
    solutionFound, solution = search(board, queenCount=1)  # Begin backtracking search
    for row in solution:
        print(row)
    result = translateCoordinate(solution, False)
    print(result)
    return result


pos, size1 = 'c0', 10  # [0,2]
queens(pos, size1)
