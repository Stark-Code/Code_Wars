def sumPermGen(n, k):
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

    # index = k-1 Moved up

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

    for y in answer:
        print(y)

    print(len(answer))
    return len(answer) + k


sumPermGen(4, 3)  # 224, 3, 120, 3
