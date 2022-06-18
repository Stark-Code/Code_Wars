import sys

def next_bigger(n):
    nStr = [x for x in str(n)]
    result = None
    for i in range(len(nStr)-1, 0, -1):
        if nStr[i] > nStr[i-1]: # [i-1] Index to be evaluated
            upperNums = nStr[:i-1]
            lowerNums = nStr[i-1:]
            minSwap = 10
            for xIdx, x in enumerate(lowerNums):
                if int(x) > int(lowerNums[0]) and int(x) < int(minSwap):
                    minSwap = x
                    minSwapIdx = xIdx
            print(lowerNums)
            print(f'minSwap: {minSwap}')
            lowerNums[0], lowerNums[minSwapIdx] = lowerNums[minSwapIdx], lowerNums[0]
            print(lowerNums)
            lowerSort = lowerNums[1:]
            lowerSort.sort()
            print(upperNums, lowerNums[0], lowerSort)
            result = upperNums + list(lowerNums[0]) + lowerSort
            print(result)
            break
    if result: return int(''.join(result))
    else: return -1


# r = next_bigger(1562)
# r = next_bigger(1234567890)
# r = next_bigger(9876543210)
r = next_bigger(59884848459853)  # 59884848493585 should equal 59884848483559
print(r)
# Find a point where a swap might occur
# This will be the swapped number
# Scan right for smallest larger number
# Swap
# Sort remaining
