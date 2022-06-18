def rangeQ(_list):
    if len(_list) == 0: return 0
    total = 0
    new_list = []
    for i in _list:
        total += i
    for i in _list:
        new_list.append(total-i)
    return abs(max(new_list) - min(new_list))
