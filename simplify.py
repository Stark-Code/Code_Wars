import re
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


def fillMissingElements(term):
    if term[0] == '': term[0] = '+'
    if term[1] == '': term[1] = '1'
    return term


def getSign(term):
    return -(int(term[1])) if term[0] == '-' else int(term[1])


def combineLikeTerms(likeComponents):
    variable = likeComponents[0][2]
    value = 0
    if len(likeComponents) == 1:
        term1 = fillMissingElements(likeComponents[0])
        term1 = getSign(term1)
        if term1 > 1: return '+' + str(term1) + variable
        elif term1 == 1: return '+' + variable
        elif term1 == -1: return "-" + variable
        else: return str(term1) + variable
    while len(likeComponents) > 1:
        term1, term2 = fillMissingElements(likeComponents[-1]), fillMissingElements(likeComponents[-2])
        term1, term2 = getSign(term1), getSign(term2)
        likeComponents.pop()
        value = term1 + term2
        print(f'{term1} + {term2} = {value}')
        likeComponents[-1] = ['', value]
    if value == 0: return ''
    elif value == 1: return variable
    else: return str(value) + variable


def simplify(poly):
    result = ''
    components = re.findall(r'(-?\d*[a-z]+)', poly)
    components = map(lambda x: "".join(x), map(lambda x: sorted(x), components))  # Sorts alphabetically
    components = map(lambda x: re.findall(r'([-+])?(\d)?([a-z]+)', x), components) # Seperates Elements
    components = list(map(lambda x: list(x[0]), components))  # Tuple to list
    logging.info(components)
    for compIdx, comp in enumerate(components):
        logging.info(comp)
        logging.info(compIdx)
        if comp == ".": continue
        likeComponents = [comp]
        for idx in range(compIdx+1, len(components)):
            if components[idx] == '.': continue
            print(f'Inner: {idx}')
            if comp[2] == components[idx][2]:
                logging.info('Match found for comp')
                likeComponents.append(components[idx])
                components[idx] = '.'
        components[compIdx] = '.'
        result += combineLikeTerms(likeComponents)
        print(result)

# simplify("dc+dcba")
simplify('-a+5ba+3a-c-2a')
# order alphabetically
# order by number of components
# combine like components


# components = map(lambda x: sorted(x), components)
# components = list(map(lambda x: "".join(x), components))