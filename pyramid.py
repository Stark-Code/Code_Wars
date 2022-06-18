from copy import deepcopy

def longest_slide_down(pyramid):
    for y in reversed(range(len(pyramid)-1)):
        for x in range(y+1):
            pyramid[y][x] += max(pyramid[y+1][x], pyramid[y+1][x+1])
    return pyramid[0][0]


T=[[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]
result = longest_slide_down(T)
print(result)