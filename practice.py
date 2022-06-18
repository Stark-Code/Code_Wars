# def hero(bullets, dragons):
#     return bullets/2 >= dragons

# def divisors(integer):
#     divArr = []
#
#     for x in range(2, integer//2+1):
#         if integer % x == 0:
#             divArr.append(x)
#
#     if len(divArr) == 0:
#         r = "{} is prime"
#         return r.format(integer)
#     else:
#         return divArr

#
# def decodeMorse(morse_code):
#     mcHash = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
#               'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
#               'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
#               'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
#               '4': '....-', '5': '.....', '6': '-....',
#               '7': '--...', '8': '---..', '9': '----.',
#               '0': '-----', ', ': '--..--', '.': '.-.-.-',
#               '?': '..--..', '/': '-..-.', '-': '-....-',
#               '(': '-.--.', ')': '-.--.-', 'SOS': '...---...'}
#
#     decoded = []
#     words = morse_code.split("   ")
#     for word in words:
#         print(word)
#         letters = word.split(" ")
#         temp = ""
#         for letter in letters:
#             decrypted = list(mcHash.keys())[list(mcHash.values()).index(letter)]
#             temp += decrypted
#         decoded.append(temp)
#
#     return ' '.join(map(str, decoded)).strip()
#
#
# decodeMorse('.... . -.--   .--- ..- -.. .')


# def tickets(people):
#     bankCash = {
#         25: 0,
#         50: 0,
#         100: 0
#         }
#     bankFunds = 0
#     result = "YES"
#
#     def createChange(bankFunds, changeOwed, changeMade):
#
#         string = "Bank Funds: {} ,  Change Owed: {}"
#         print(string.format(bankFunds, changeOwed))
#
#         if bankFunds <= 0:
#             print("No Money in Bank")
#             return "NO"
#         if changeOwed == 0:
#             print("Correct Change Given")
#             return "YES"
#         if not changeMade:
#             return "NO"
#         changeMade = False
#         if changeOwed == 75:
#             if bankCash[50] > 0:
#                 changeOwed -= 50
#                 bankCash[50] -= 1
#                 bankFunds -= 50
#                 changeMade = True
#         if changeOwed == 50 or changeOwed == 75:
#             if bankCash[25] > 0:
#                 changeOwed -= 25
#                 bankCash[25] -= 1
#                 bankFunds -= 25
#                 changeMade = True
#         if changeOwed == 25:
#             if bankCash[25] > 0:
#                 changeOwed -= 25
#                 bankCash[25] -= 1
#                 bankFunds -= 25
#                 changeMade = True
#         return createChange(bankFunds, changeOwed, changeMade)
#
#     for cashGiven in people:
#         bankCash[cashGiven] += 1
#         changeOwed = cashGiven - 25
#         bankFunds += cashGiven
#
#         if changeOwed >= 0 and result != "NO":
#             result = createChange(bankFunds, changeOwed, True)
#             print(result)
#     return result
#
#
# #tickets([25, 25, 50]) # => YES
# tickets([25, 100]) # => NO. will not have enough money to give change to 100 dollars
# #tickets([25, 25, 50, 50, 100]) #No

# def dist(v, mu):
#     d1 = v/3.6
#     return (v*v)/(3.6*3.6) / (2 * mu * 9.81) + d1
#
#
# result = dist(144, 0.3)  # 311.83146449201496
# print(result)
#
#
# def speed(d, mu):
#
#
# speed(159, 0.8)  # 153.79671564846308


#
#
# def street_fighter_selection(fighters, initial_position, moves):
#     selected = []
#     newPos = [initial_position[0], initial_position[1]]
#     for pos in moves:
#
#         if pos == 'left':
#             newPos[0] -= 1
#             if newPos[0] == -1:
#                 newPos[0] = 5
#         if pos == 'right':
#             newPos[0] += 1
#             if newPos[0] == 6:
#                 newPos[0] = 0
#         if pos == 'up':
#             newPos[1] -= 1
#             if newPos[1] == -1:
#                 newPos[1] = 0
#         if pos == 'down':
#             newPos[1] += 1
#             if newPos[1] == 2:
#                 newPos[1] = 1
#         selected.append(fighters[newPos[1]][newPos[0]])
#         print(selected)
#     return selected
#
#
# fighters = [['Ryu', 'E.Honda', 'Blanka', 'Guile', 'Balrog', 'Vega'], ['Ken', 'Chun Li', 'Zangief', 'Dhalsim', 'Sagat', 'M.Bison']]
# initial_position = (0, 0)
# moves = ['up', 'up', 'up', 'up']
# street_fighter_selection(fighters, initial_position, moves)

# iterate through moves array - Add values to x and y position of newPos accordingly
# If position Is at 0 and we move left, position is at end. If position is at end and move right, pos at beg
# If position is down and move up,
# Evaluate position, add character to array list.


#
# def super_street_fighter_selection(fighters, initial_position, moves):
#     selected = []
#     newPos = [initial_position[1], initial_position[0]]
#
#     print(fighters[newPos[0]][newPos[1]])
#     for pos in moves:
#
#         def moveLeft():
#             print("Moving Left")
#             newPos[0] -= 1
#             if newPos[0] == -1:
#                 newPos[0] = len(fighters[newPos[1]]) - 1
#             if fighters[newPos[1]][newPos[0]] == "":
#                 moveLeft()
#         if pos == 'left':  # Handles Grid Size
#             moveLeft()
#
#         def moveRight():
#             print("Moving Right")
#             newPos[0] += 1
#             if newPos[0] == len(fighters[newPos[1]]):
#                 newPos[0] = 0
#             if fighters[newPos[1]][newPos[0]] == "":
#                 moveRight()
#         if pos == 'right':  # Handles Grid Size
#             moveRight()
#
#         if pos == 'up':  # Handles Grid Size & Spaces
#             print("Moving Up")
#             currPos = newPos[1]
#             newPos[1] -= 1
#             if newPos[1] == -1:
#                 newPos[1] = 0
#             if fighters[newPos[1]][newPos[0]] == "":
#                 print("X Found")
#                 newPos[1] = currPos
#
#         if pos == 'down':  # Handles Grid Size & Spaces
#             print("Moving Down")
#             currPos = newPos[1]
#             newPos[1] += 1
#             if newPos[1] == len(fighters):
#                 newPos[1] -= 1
#             if fighters[newPos[1]][newPos[0]] == "":
#                 newPos[1] = currPos
#
#         selected.append(fighters[newPos[1]][newPos[0]])
#         print(selected)
#     return selected
#
#
# fighters = [['', 'Ryu', 'E.Honda', 'Blanka', 'Guile', ''],
#             ['Balrog', 'Ken', 'Chun Li', 'Zangief', 'Dhalsim', 'Sagat'],
#             ['Vega', 'T.Hawk', 'Fei Long', 'Deejay', 'Cammy', 'M.Bison']]
# initial_position = (1, 5)
# moves = ["up"]*4
# super_street_fighter_selection(fighters, initial_position, moves)
#
# #Deal with mutatable grid sizes
# # Deal with spaces
# # Move right, see a space, move right again
# #Move up, down See a space. Do nothing


# def is_triangular(t):
#     max = t*2
#     val = 1
#     total = 1
#     result = False
#     while total < max:
#         total = val * (val + 1)/2
#         print(val)
#         val += 1
#         if t == total:
#             print("Triangular Number Found!")
#             result = True
#             break
#     return result
# is_triangular(20)

# T(n) = n * (n + 1) / 2
#
# def calculate_winners(snapshot, penguins):
#     lanes = snapshot.split("\n")
#     penDist = []
#     penPos = []
#     winners = []
#     for x in lanes:
#         pos = x.find("p")
#         if pos == -1:
#             pos = x.find("P")
#         penPos.append(pos)
#
#     for i in range(len(penPos)):
#         penDist.append(lanes[i].count("-", penPos[i]))
#         penDist[i] += (lanes[i].count("~", penPos[i]))*2
#
#     penDistCopy = penDist.copy()
#     penDistCopy.sort()
#
#     for i in penDistCopy:
#         winners.append(penguins[penDist.index(i)])
#
#     winStr = 'GOLD: {}, SILVER: {}, BRONZE: {}'
#     winStr = winStr.format(winners[0], winners[1], winners[2])
#     return winStr
#
#
#
# snapshot = """|----p---~---------|
# |----p---~~--------|
# |----p---~~~-------|"""
# penguins = ["Derek", "Francis", "Bob"]
# calculate_winners(snapshot, penguins)

# 9.2 D Weight
# [[(1, 1), (2, 1)], [(2, 2), (3, 2)]]
#
# def josephus(items, k):
#     permuted = []
#     elementPos = 0
#     initLength = len(items)
#
#     while len(permuted) < initLength:
#
#         legalMoves = 0
#
#         def checkInitPos(arg_elementPos, arg_legalMoves):
#             if arg_elementPos >= len(items):
#                 arg_elementPos -= initLength
#             if items[arg_elementPos] == "":
#                 arg_elementPos += 1
#                 return checkInitPos(arg_elementPos, arg_legalMoves)
#             else:
#                 arg_legalMoves += 1
#                 return arg_elementPos, arg_legalMoves
#
#         while legalMoves < k-1:
#             elementPos, legalMoves = checkInitPos(elementPos + 1, legalMoves)
#
#         permuted.append(items[elementPos])
#         items[elementPos] = ""
#
#         if len(permuted) < initLength:
#             while items[elementPos] == "":
#                 elementPos += 1
#                 if elementPos >= len(items):
#                     elementPos -= initLength
#
#     return permuted
#
#
# josephus([1, 2, 3, 4, 5, 6, 7], 3)

#
# def josephus_survivorCheck(lx, k):
#     permuted = []
#     elementPos = 0
#
#     items = []
#     for x in range(1, lx + 1):
#         items.append(x)
#
#     initLength = len(items)
#
#     while len(permuted) < initLength:
#
#         legalMoves = 0
#
#         def checkInitPos(arg_elementPos, arg_legalMoves):
#             if arg_elementPos >= len(items):
#                 arg_elementPos -= initLength
#             if items[arg_elementPos] == "":
#                 arg_elementPos += 1
#                 return checkInitPos(arg_elementPos, arg_legalMoves)
#             else:
#                 arg_legalMoves += 1
#                 return arg_elementPos, arg_legalMoves
#
#         while legalMoves < k-1:
#             elementPos, legalMoves = checkInitPos(elementPos + 1, legalMoves)
#
#         permuted.append(items[elementPos])
#         items[elementPos] = ""
#
#         if len(permuted) < initLength:
#             while items[elementPos] == "":
#                 elementPos += 1
#                 if elementPos >= len(items):
#                     elementPos -= initLength
#
#     return permuted[-1]
#
#
# for n in range(1, 65):
#     result = josephus_survivorCheck(n, 2)
#     print(f"n: {n}, k: 3, {result}")
# # 4, 3 > 1
# # 5, 3, > 4
# # 6, 3 > 1
# # 7, 3 > 4
# # 8, 3, > 7
# # 9, 3 > 1
# # 10, 3 > 4
# # 11, 3 > 7
# # 12, 3 > 10
# # 13, 3 > 13
# # 14, 3 > 2
# # 15, 3 > 5
# # 16, 3 > 8
#
#
# def josephusSurvivor(groupSize, survivor):
#     pass
#
#
# josephusSurvivor(7, 3)
#
#
# def all_continents(lst):
#
#     lanCount = 0
#     mainLan = lst[0]["language"]
#     for obj in lst:
#         if obj["language"] == mainLan:
#             lanCount += 1
#
#     if lanCount == len(lst):
#         return True
#     else:
#         False
#
#
# list1 = [
#     {'firstName': 'Fatima', 'lastName': 'A.', 'country': 'Algeria', 'continent': 'Africa', 'age': 25,
#      'language': 'JavaScript'},
#     {'firstName': 'Agustín', 'lastName': 'M.', 'country': 'Chile', 'continent': 'Americas', 'age': 37, 'language': 'C'},
#     {'firstName': 'Jing', 'lastName': 'X.', 'country': 'China', 'continent': 'Asia', 'age': 39, 'language': 'Ruby'},
#     {'firstName': 'Laia', 'lastName': 'P.', 'country': 'Andorra', 'continent': 'Europe', 'age': 55, 'language': 'Ruby'},
#     {'firstName': 'Oliver', 'lastName': 'Q.', 'country': 'Australia', 'continent': 'Oceania', 'age': 65,
#      'language': 'PHP'}
# ]
#
# all_continents(list1)


