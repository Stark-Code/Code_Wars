def solution(string, markers):
    strList = string.splitlines(keepends=False)
    stripped = []
    print(strList)
    for marker in markers:
        markerLoc = None
        for _str in strList:
            try:
                markerLoc = _str.index(marker)
            except ValueError:
                pass
            if markerLoc:
                stripped.append(_str[:markerLoc] + "\\n")
    print(stripped)
    result = "".join(stripped)
    return result[:-2]

r = solution("apples, pears # and bananas\ngrapes\nbananas", ["#", "!"])
print(r)
# "apples, pears\ngrapes\nbananas"