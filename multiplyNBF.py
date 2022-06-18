# If the prime number length is the same, the final answer is the same.
# Clearly a counting problem
# 2, 3, 5, 7 and 2, 3, 5, 11 produce the same answer. 81

def multiply(n, k):

    multiArr = []
    check = True
    for i in range(k):
        multiArr.append(1)
    answer = []
    index = k - 1

    def checkProduct(arr, arg_check):
        result = 1
        for x in arr:
            result *= x
        if result == n:
            answer.append(arr.copy())
        if result > n:
            arg_check = False
        return arg_check
    # index = k-1 Moved up

    while multiArr[0] != n//2+1:
        if multiArr[index] == n//2+1:
            check = True
            multiArr[index] = 1
            if index > 0:
                index -= 1
        else:
            multiArr[index] += 1
            if check:
                check = checkProduct(multiArr, check)
            index = len(multiArr)-1


    for x in answer:
        print(x)
    # print(answer)
    print(f"Answer: {len(answer)} (Edge Case not included)")
    return len(answer) + k


multiply(180, 5)  # 224, 3, 120, 3

primes = []


def findPrimes(num, divisor):
    while divisor <= num:
        if num % divisor == 0:
            primes.append(divisor)
            num = num / divisor
        else:
            divisor += 1


findPrimes(180, 2)
#
print(primes)


# For prime trees with repetition:
# Calculate total permutations with ones as normal
# Calculate total permutations without one
# Calculate

