import copy
import time
import border
import sys


def converge(_g, u1, u2, u3):
    connections = {x: list(_g[x]) for x in _g if x in [u1, u2, u3]}
    if u1 == u2 == u3: return 0
    step = 1
    while True:
        intersection = set.intersection(set(connections[u1]), set(connections[u2]), set(connections[u3]))
        if intersection:
            return step
        else: step += 1
        if step > 50: return None

        for node in connections:
            temp = []
            for edge in set(connections[node]):
                temp.extend(list(_g[edge]))
            connections[node] = temp


g1 = {
    0: {5, 1, 3},
    1: {0, 2},
    2: {1},
    3: {0, 4},
    4: {3},
    5: {6, 0},
    6: {5},
}

g2 = {
            1: {2, 3},
            2: {1, 3},
            3: {1, 2},
        }

g3 = {1: {2}, 2: {1, 3}, 3: {2}}
#123

border.printBorder()
tic = time.perf_counter()
# converge(g1, 2, 4, 6)  # 2
# converge(g2, 1, 2, 3)
converge(g3, 1, 2, 3)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")


