import time

def insertionSort(_list, value):
    _list.append(value)
    print(f'Unsorted List: {_list}')
    idx = -2
    while _list[idx+1] < _list[idx]:
        _list[idx+1], _list[idx] = _list[idx], _list[idx+1]
        idx -= 1
    return _list
    print(f'Sorted List: {_list}')


tic = time.perf_counter()
test = [1, 2, 3, 4, 5, 7, 8, 9, 10]
insertionSort(test, 6)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")


