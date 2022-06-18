import time
factorialList = {
    1: 1,
    2: 2,
    3: 6,
    4: 24,
    5: 120,
    6: 720,
    7: 5040,
    8: 40320,
    9: 362880,
    10: 3628800,
    11: 39916800,
    12: 479001600,
    13: 6227020800,
    14: 87178291200,
    15: 1307674368000,
    16: 20922789888000,
    17: 355687428096000,
    18: 6402373705728000,
    19: 121645100408832000,
    20: 2432902008176640000,
    21: 51090942171709440000,
    22: 1124000727777607680000,
    23: 25852016738884976640000,
    24: 620448401733239439360000,
    25: 15511210043330985984000000,
}


def calculatePermutations(factorial, repeats):
    print(f'Factorial: {factorial}')
    print(f'Repeats: {repeats}')
    repeatTotal = 1
    permutations = factorialList[factorial]
    for repeat in repeats:
        repeatTotal *= factorialList[repeat]
    print(permutations / repeatTotal)
    return permutations / repeatTotal


def listPosition(word):
    sortedWord = sorted(word)
    counts = dict()
    build = ""
    positionFormula = []
    lastVisited = -1
    for i in sortedWord:
        counts[i] = counts.get(i, 0) + 1
    print(f'Sorted Word: {sortedWord}')
    print(f'Counts: {counts}')

    while word:
        # print(positionFormula)
        # print(f'word: {word}')

        for letter in sortedWord:
            print(f"Checking {letter}")
            if letter == lastVisited or letter == word[0]:
                print(f'letter {letter} is equal to last visited {lastVisited}')
                if letter == word[0]:
                    build += letter
                    print(f'Correct letter found; Build: {build}')
                    sortedWord.pop(sortedWord.index(letter))
                    print(f"Removing {letter} from {sortedWord}")
                    word = word[1:]
                    counts[letter] -= 1
                    lastVisited = -1
                    break
                continue


            print(f'sortedWord: {sortedWord}')
            print(f'Counts: {counts}')
            factorialSum = 0
            repetitions = []

            lastVisited = letter
            counts[letter] -= 1
            print(f'# 1 subtracted from {letter} : {counts} : {counts[letter]}')
            for letterCount in counts:
                print(f'letterCount : {letterCount} : {counts[letterCount]}')
                factorialSum += counts[letterCount]
                print(f'Factorial Sum : {factorialSum}')
                if counts[letterCount] > 1:
                    repetitions.append(counts[letterCount])
                    print(f"Repetion Found: {repetitions}")
            result = calculatePermutations(factorialSum, repetitions)
            positionFormula.append(result)
            counts[letter] += 1

    total = 1
    print(f'Pos Formula: {positionFormula}')
    for num in positionFormula:
        total += num
    print(f"Position in List: {total}")
    return total

tic = time.perf_counter()
listPosition('booo')
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")
# listPosition("question")
# listPosition('bookkeeper')

