def addElements(low, high, numList, result):
    if high - low >= 3: # 3 length + sequence found. Record full sequence
        result.append(f'{numList[low]}-{numList[high - 1]}')
    else:
        for idx in range(low, high):
            result.append(str(numList[idx]))
    low, high = high, high + 1
    print(result)
    return low, high


def solution(numList):
    low, high = 0, 1
    result = []
    while True:
        if numList[high] - numList[high - 1] == 1:  # Sequential Numbers Found
            high += 1
            if high == len(numList) - 1:
                addElements(low, high+1, numList, result)
                break
        else:
            low, high = addElements(low, high, numList, result)
    return ','.join(result)

solution(([-6, -3, -2, -1, 0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20]))
