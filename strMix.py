from collections import Counter
import re


def strCompare(str1, str2, tarIndex):
    argResult = []
    delArr = []
    for key in str1:
        if key in str2:
            if str1[key] > str2[key] and str1[key] > 1:
                argResult.append(f"{tarIndex}:" + key * str1[key])
                delArr.append(key)
            if str1[key] == str2[key] and str1[key] > 1:
                argResult.append("=:" + key * str1[key])
                delArr.append(key)
        if key not in str2:
            if str1[key] > 1:
                argResult.append(f"{tarIndex}:" + key * str1[key])
                delArr.append(key)
    return argResult, delArr


def sort(sortedArr, index):
    if index == 0:
        return sortedArr
    if len(sortedArr[index]) > len(sortedArr[index - 1]):
        sortedArr[index], sortedArr[index - 1] = sortedArr[index - 1], sortedArr[index]
        index -= 1
        return sort(sortedArr, index)
    if len(sortedArr[index]) == len(sortedArr[index - 1]):
        if sortedArr[index][0] < sortedArr[index - 1][0]:
            sortedArr[index], sortedArr[index - 1] = sortedArr[index - 1], sortedArr[index]
        if sortedArr[index - 1][0] == '=':
            sortedArr[index], sortedArr[index - 1] = sortedArr[index - 1], sortedArr[index]
        if sortedArr[index][0] == sortedArr[index - 1][0]:
            if sortedArr[index][2] < sortedArr[index - 1][2]:
                sortedArr[index], sortedArr[index - 1] = sortedArr[index - 1], sortedArr[index]
        index -= 1
        return sort(sortedArr, index)
    return sortedArr


def mix(s1, s2):
    if s1 == s2:
        return ""
    s1 = re.sub('[A-Z0-9\W]', '', s1)
    s2 = re.sub('[A-Z0-9\W]', '', s2)
    s1Count, s2Count = Counter(s1.replace(" ", "")), Counter(s2.replace(" ", ""))
    result, delArr = strCompare(s1Count, s2Count, "1")

    for x in delArr:
        if x in s1Count:
            del s1Count[x]
        if x in s2Count:
            del s2Count[x]
    result2, delArr2 = strCompare(s2Count, s1Count, "2")
    result.extend(result2)  # Spread
    sortedArr = [result[0]]
    result.pop(0)
    for item in result:
        sortedArr.append(item)
        sortedArr = sort(sortedArr, len(sortedArr) - 1)
    separator = "/"
    sortedStr = separator.join(sortedArr)
    return sortedStr


mix("Are they here", "yes, they are here")
