def binarySearch(num, low, high, searchList):
    mid = (high + low) // 2
    print(searchList[mid])
    if searchList[mid] == num:
        print('Number Found!')
        return mid
    elif searchList[mid] > num:
        high = mid
        return binarySearch(num, low, high, searchList)
    elif searchList[mid] < num:
        low = mid
        return binarySearch(num, low, high, searchList)


# sL = [i for i in range(100)]
sL = [1, 3, 4, 6, 8, 9, 13, 15, 17, 18, 19, 23, 28, 39, 49, 56, 57, 61, 62, 65, 69, 73]
result = binarySearch(17, 0, len(sL)-1, sL)
print(f'Result: {result}')