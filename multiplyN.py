import math


def genCombinations(n, k):
    sumArr = []
    check = True
    for i in range(k):
        sumArr.append(1)
    answer = []
    index = k - 1

    def checkSum(arr, arg_check):
        result = 0
        for x in arr:
            result += x
        if result == n:
            answer.append(arr.copy())
        if result > n:
            arg_check = False
        return arg_check

    while sumArr[0] != n:
        if sumArr[index] == n:
            check = True
            sumArr[index] = 1
            if index > 0:
                index -= 1
        else:
            sumArr[index] += 1
            if check:
                check = checkSum(sumArr, check)
            index = len(sumArr) - 1

    return answer


def findPrimes(num, divisor):
    primes = []
    while divisor <= num:
        if num % divisor == 0:
            primes.append(divisor)
            num = num / divisor
        else:
            divisor += 1
    return primes


def nChooseK(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def genPermutations(n, combinations):
    result = 0
    for bP in combinations:
        nCopy = n
        numPermutations = 1
        print(f"Checking: {bP}")
        for k in bP:
            numPermutations *= nChooseK(nCopy, k)
            nCopy -= k
        print(f"numPermutations: {numPermutations}")
        result += numPermutations
    print(result)
    return result


def multiply(n, k):

    # Find the primes of n
    primeList = findPrimes(n, 2)
    primeListLen = len(primeList)
    print(f"primeList: {primeList}, Length: {primeListLen}")

    # Find all the permutations for splitting a list into groups of k
    primeCombinations = genCombinations(primeListLen, k)
    print(primeCombinations)

    primePermutations = genPermutations(primeListLen, primeCombinations)

    for i in range(k-2+1):
        primeListLen += i

    print(f"Appended List Length: {primeListLen}")

    primeCombinationsWithOne = genCombinations(primeListLen, k)
    print(primeCombinationsWithOne)

    primeOnePermutations = genPermutations(primeListLen, primeCombinationsWithOne)
    print(primeOnePermutations - (primePermutations*2) + k)
    return primeOnePermutations - (primePermutations*2) + k


multiply(60, 3)

#
# 2, 2, 3, 5 = 60
# Remove identical permutations by dividing by factorial of identical values

# First set = 18

# 50 - x - x - x = 27

# I think I need to go through the combination lists and divide out x! [2, 2, 2, 3] 3! out of each list where
# 2 single elements appear
# DW 164.6
