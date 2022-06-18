orig_print = print

def blockPrint():
    global print
    print = lambda *args, **kwargs: None

def enablePrint():
    global print
    print = orig_print