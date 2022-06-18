import copy

adjList = {
    '1': ['1', '2', '4'],
    '2': ['1', '2', '3', '5'],
    '3': ['2', '3', '6'],
    '4': ['1', '4', '5', '7'],
    '5': ['2', '4', '5', '6', '8'],
    '6': ['3', '5', '6', '9'],
    '7': ['4', '7', '8'],
    '8': ['5', '7', '8', '9', '0'],
    '9': ['6', '8', '9'],
    '0': ['0', '8']
}


def dfs(observed, permutation, idx, solution):
    if len(permutation) == len(observed):
        solution.append(permutation)
        return
    permutationClone = copy.copy(permutation)
    for i in adjList[observed[idx]]:
        permutationClone += i
        dfs(observed, permutationClone, idx+1, solution)
        permutationClone = permutation
    return solution


def get_pins(observed):
    return dfs(observed, '', 0, solution=[])


r = get_pins('369')
print(f'Solution: {r}')



xList = ['236', '238', '239', '256', '258', '259','266', '268', '269','296', '298', '299','336', '338', '339','356','358', '359','366', '368', '369', '396', '398', '399', '636', '638', '639', '656', '658', '659', '666', '668', '669',  '696', '698', '699']


yList = ["339","366","399","658","636","258","268","669","668","266","369","398","256","296","259","368","638","396","238","356","659","639","666","359","336","299","338","696","269","358","656","698","699","298","236","239"]


for x in xList:
    if x not in yList:
        print('Value not found')
print(f'{len(xList) == len(yList)} ')