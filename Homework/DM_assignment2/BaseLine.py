
def loadDataSet():
    return [[1,2,5], [2,4], [2,3], [1,2,4],[1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]

def iterSet(prefix, trans, pos, result, put):
    if pos >= len(trans):
        return
    prefixCopy = prefix.copy()
    if put == True:
        prefixCopy.add(trans[pos])
        froz = frozenset(prefixCopy)
        if froz not in result.keys():
            result[froz] = 1
        else:
            result[froz] = result[froz] + 1
    iterSet(prefixCopy, trans, pos + 1, result, True)
    iterSet(prefixCopy, trans, pos + 1, result, False)




if __name__ == '__main__':

    dataSet = loadDataSet()
    result = {}
    for trans in dataSet:
        iterSet(set([]), trans, 0, result, True)
        iterSet(set([]), trans, 0, result, False)
    minSup = 2
    for itemSet in list(result.keys()):
        if result[itemSet] < minSup:
            del(result[itemSet])
    # print(result)
    print(result.keys())