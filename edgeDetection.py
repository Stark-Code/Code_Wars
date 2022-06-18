def searchHelper(currNode, image, searchList, maxVal):
    for x in searchList:
        if 0 <= x[0] < len(image) and 0 <= x[1] < len(image[0]):
            temp = abs(image[currNode[0]][currNode[1]] - image[x[0]][x[1]])
            if temp > maxVal:
                maxVal = temp
    return maxVal


def searchAdj(currNode, image, history, edgeDetList):  # [y, x]
    searchList = []
    left, right = [currNode[0], currNode[1] - 1], [currNode[0], currNode[1] + 1]
    up, down = [currNode[0] - 1, currNode[1]], [currNode[0] + 1, currNode[1]]
    upLeft, upRight = [currNode[0] - 1, currNode[1] - 1], [currNode[0] - 1, currNode[1] + 1]
    downLeft, downRight = [currNode[0] + 1, currNode[1] - 1], [currNode[0] + 1, currNode[1] + 1]

    if history is not None:
        searchList.extend((upRight, right, downRight))
        maxVal = searchHelper(currNode, image, searchList, history)
        edgeDetList.append(maxVal)
        return None, edgeDetList

    elif currNode[1] < len(image[currNode[0]]) - 1:
        if image[currNode[0]][currNode[1]] == image[currNode[0]][currNode[1]+1]:  # Create History
            searchList.extend((up, upRight, downRight, down))
            history = searchHelper(currNode, image,  searchList, 0)
            searchList.clear()
            searchList.extend((upLeft, left, downLeft))
            maxVal = searchHelper(currNode, image, searchList, history)
            edgeDetList.append(maxVal)
            return history, edgeDetList
        else:
            searchList.extend((left, upLeft, up, upRight, right, downRight, down, downLeft))
            maxVal = searchHelper(currNode, image, searchList, 0)
            edgeDetList.append(maxVal)
            return None, edgeDetList
    else:
        searchList.extend((left, upLeft, up, upRight, right, downRight, down, downLeft))
        maxVal = searchHelper(currNode, image, searchList, 0)
        edgeDetList.append(maxVal)
        return None, edgeDetList


def edge_detection(image):
    data = image.split(" ")
    rows = int(data[0])
    dataIdx = 1
    pixList = []
    edgeDetList = []
    while dataIdx <= len(data) - 3:
        pixList.append([])
        colCount = 0
        while colCount < rows:
            if int(data[dataIdx + 1]) > 0:
                pixList[-1].append(int(data[dataIdx]))
                data[dataIdx + 1] = int(data[dataIdx + 1]) - 1
                colCount += 1
            else:
                dataIdx += 2
    print(pixList)
    history = None
    for yIdx in range(len(pixList)):
        for xIdx in range(len(pixList[yIdx])):
            history, edgeDetList = searchAdj([yIdx, xIdx], pixList, history, edgeDetList)
            print(edgeDetList)
    result = f'{rows} '
    count = 1
    for idx in range(len(edgeDetList)-1):
        print(f"Result: {result}")
        val = edgeDetList[idx]
        if val == edgeDetList[idx + 1]:
            count += 1
        else:
            result += f"{val} " + f"{count} "
            count = 1
        if idx == len(edgeDetList) - 2:
            result += f"{val} " + f"{count}"
    print(f"Final: {result}")
    return result

image1 = '3 255 1 10 1 255 2 10 1 255 2 10 1 255 1'
image = '7 15 4 100 15 25 2 175 2 25 5 175 2 25 5'
image2 = '10 35 500000000 200 500000000'
image3 = '10 20 1 3 50 20 49'
edge_detection(image3)

'10 17 2 0 8 17 2 0 28 17 22 0 38'