# def gangs(divisors, k):
#
#     gangId = {}
#
#     for i in range(1, k+1):
#         gID = ""
#         for j in divisors:
#             if i % j == 0:
#                 gID += str(j)
#         if gID not in gangId:
#             gangId.update({gID: [i]})
#         else:
#             gangId[gID].append(i)
#
#         # print(f"k num: {i}, id: {gID}")
#         # print(len(gangId))
#     return len(gangId)
# gangs([2, 3, 6, 5], 15)


# Move through list 1 - k. Test against each number in divisors. Add an id to each number as it passes test. Add id to
# Dictionary and associate it with the value in the list.

# def parts_sums(ls):
#     total = 0
#     sumArr = []
#     for x in ls:
#         total += x
#     sumArr.append(total)
#     for y in ls:
#         total -= y
#         sumArr.append(total)
#     return sumArr
# parts_sums([0, 1, 3, 6, 10])

#
# def generate_hashtag(s):
#
#     strArr = s.strip().title().split()
#     print(strArr)
#     if s == "" or len(s) > 140:
#         return False
#     strArr[0] = "#" + strArr[0]
#     print(strArr)
#     hashTag = ""
#     for word in strArr:
#         hashTag += word
#     return hashTag
#
# generate_hashtag("      Hello there thanks for trying my Kata  ")

#
# def findPrime(num):
#     divisor = 2
#     primes = []
#     while divisor <= num:
#         if num % divisor == 0:
#             primes.append(divisor)
#             num = num / divisor
#         else:
#             divisor += 1
#     if len(primes) == 1:
#         return True
#
#
# def millerRabin(num):
#     print(f"Checking {num}")
#
#     def findD(argR, numLessOne):  # Recursive, num is num - 1
#         argD = numLessOne // (2 ** argR)
#         print(argR, numLessOne)
#         if argD % 2 != 0:
#             return argD, argR
#         else:
#             return findD(argR + 1, numLessOne)
#
#     d, r = findD(1, num - 1)
#
#     # Pick random number a
#     def findRandomNumber(numberLessTwo):
#         import random
#         return random.randint(2, numberLessTwo)
#
#     a = findRandomNumber(num - 2)
#
#     x = a ** d % num
#
#     if x == 1 or x == num - 1:
#         return True
#     elif x * x % num == num - 1:
#         return True
#
#     for i in range(1, r):
#         x = (x * x) % num
#         if x == num - 1:
#             return True
#         if x == 1:
#             return False
#
#
#
# def next_prime(number):
#     if number == 0:
#         return 2
#     if number == 1:
#         return 2
#     if number == 2:
#         return 3
#     if number == 3:
#         return 5
#     flag = False
#
#     while not flag:
#         if number % 2 == 0:
#             number += 1
#         elif number % 5 == 0:
#             number += 2
#         else:
#             number += 2
#         flag = millerRabin(number)
#     return number
#
#
# result = next_prime(13)
# print(result)
# #
# # 1) Pick a random number 'a' in range [2, n-2]
# # 2) Compute: x = pow(a, d) % n
# # 3) If x == 1 or x == n-1, return true.
# #
# # // Below loop mainly runs 'r-1' times.
# # 4) Do following while d doesn't become n-1.
# #      a) x = (x*x) % n.
# #      b) If (x == 1) return false.
# #      c) If (x == n-1) return true.

# def sum_square_even_root_odd(nums):
#     import math
#     sum = 0
#     for x in nums:
#         if x == 0:
#             continue
#         if x % 2 == 0:
#             sum += x ** 2
#         else:
#             sum += math.sqrt(x)
#     return round(sum, 2)
#
#
# sum_square_even_root_odd([4,5,7,8,1,2,3,0]) #91.61
#
# def make_a_window(num):
#
#     window = [[]]
#     for top in range(num * 2 + 3):
#         window[-1].append("-")
#     for upper in range(num):
#         window.append([])
#         for x in range(2):
#             window[-1].append("|")
#             for y in range(num):
#                 window[-1].append(".")
#         window[-1].append("|")
#     # Middle
#     window.append(["|"])
#     for x in range(num):
#         window[-1].append("-")
#     window[-1].append("+")
#     for x in range(num):
#         window[-1].append("-")
#     window[-1].append("|")
#     # Bottom
#     for lower in range(num):
#         window.append([])
#         for x in range(2):
#             window[-1].append("|")
#             for y in range(num):
#                 window[-1].append(".")
#         window[-1].append("|")
#     window.append([])
#     for bottom in range(num * 2 + 3):
#         window[-1].append("-")
#     windowString = ""
#     for row in window:
#         windowString += "".join(row)
#         windowString += "\n"
#     windowString = windowString[:-1]
#     return windowString
#
#
# make_a_window(3)

# def make_a_window(n):
#     top     = '-' * (2*n+3)
#     middle  = f"|{ '-'*n }+{ '-'*n }|"
#     glasses = [f"|{ '.'*n }|{ '.'*n }|"] * n
#     return '\n'.join([top, *glasses, middle, *glasses, top])


# def next_prime(number):
#     print(number)
#     if number == 0:
#         return 2
#     if number == 1:
#         return 2
#     if number == 2:
#         return 3
#     primeFound = False
#     number += 1
#     if number % 2 == 0:
#         number += 1
#
#     def checkPrime(primeCandidate, argPrimeFound):
#         print(f"Factoring: {primeCandidate}")
#         f = 3
#         while f * f <= primeCandidate:
#             if primeCandidate % f == 0:
#                 primeCandidate += 2
#                 return primeCandidate, False
#             else:
#                 f += 2
#         return primeCandidate, True
#
#     while not primeFound:
#         number, primeFound = checkPrime(number, primeFound)
#     print(number)
#     return number
#
#
# next_prime(17)
#
# def eratosthenesSieve(limit):
#     markArr = [True for i in range(limit)]
#
#     for p in range(2, limit - 1):
#
#         if not markArr[p]:
#             continue
#         inc = p
#         inc += p
#         while inc < limit:
#             markArr[inc] = False
#             inc += p
#
#     for i in range(len(markArr)):
#         if markArr[i]:
#             print(i, end=",")
#
#
# # eratosthenesSieve(100)
#
# def segmentedSieve():
#     pass
#
#
# segmentedSieve(100)
# print(i, end=",")