import time
import math
# import memory_profiler as mem_profile


def eratosthenesSieve(limit):
    markArr = [True for i in range(limit)]

    for p in range(2, limit - 1):

        if not markArr[p]:
            continue
        inc = p
        inc += p
        while inc < limit:
            markArr[inc] = False
            inc += p
    prime = []
    for i in range(len(markArr)):
        if markArr[i]:
            prime.append(i)
    # Remove 0 and 1 from prime Array
    prime.remove(prime[0])
    prime.remove(prime[0])

    return prime

prime = eratosthenesSieve(limit)


def segmentedSieve(n, prime):
    limit = n // 4

    # Create prime array to start

    #  Segment Start
    low = limit + 1

    while low <= n:

        markArr = [True for i in range(limit)]

        for p in prime:
            if p > math.sqrt(low + limit + 1):
                break
            startP = (low // p) * p
            if startP < low:
                startP += p
            markX = startP - low
            while markX <= len(markArr) - 1:
                markArr[markX] = False
                markX += p

        for i in range(len(markArr)):
            if markArr[i]:
                prime.append(i + low)
        low += limit
    # print(prime)
    print(len(prime))


# print('Memory before: {}Mb'.format(mem_profile.memory_usage()))
start = time.perf_counter()
segmentedSieve(1000, prime)
end = time.perf_counter()
# print(f"Primes calculated in {end - start:0.4f} seconds")
# print('Memory After: {}Mb'.format(mem_profile.memory_usage()))
#
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# 1, 2, 3, 4, 5, 6, 7, 8, 9, 10


