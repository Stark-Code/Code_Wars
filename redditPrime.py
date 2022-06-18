import time
import math

def eratosthenesSieve(limit):
    markArr = [True for i in range(limit + 1)]  # Inclusive of limit
    markArr[0] = False  # 0 not prime
    markArr[1] = False  # 1 not prime

    for p in range(len(markArr)):
        if not markArr[p]:
            continue
        inc = 2 * p

        while inc <= limit:
            markArr[inc] = False
            inc += p

    prime = []
    for i in range(len(markArr)):
        if markArr[i]:
            prime.append(i)
    return prime


def segmentedSieve_mod(n):
    limit = int(math.floor(math.sqrt(n)))
    prime = eratosthenesSieve(limit)

    low = limit + 1

    while low < n:
        # Handles partial segment at end
        markArr = [True for i in range(min(limit, n - low))]

        for p in prime:
            # Primes too large to find multiple not already seen
            if p > math.sqrt(low + limit + 1):
                break
            if low % p == 0:
                x = 0
            else:
                x = p - low % p  # Jump ahead to where (low+x)%p is 0

            while x <= len(markArr) - 1:
                markArr[x] = False
                x += p

        for i in range(len(markArr)):
            if markArr[i]:
                prime.append(i + low)

        low += limit
    print(len(prime))
    return prime


start = time.perf_counter()
segmentedSieve_mod(10000000)
end = time.perf_counter()
print(f"Primes calculated in {end - start:0.4f} seconds")