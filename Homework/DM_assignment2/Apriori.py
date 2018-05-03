import time
import json



def loadDataSet():
    # thing_arr = []
    #
    # with open('data/Groceries.txt', 'r') as f:
    #     X = f.read()
    #     thing_arr = json.loads(X)
    #     f.close()
    # return thing_arr


  return [[1,2,5], [2,4], [2,3], [1,2,4],[1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]

def loadMap():

    thing_dic = {}
    with open('data/Groceries_to_int.txt', 'r') as f:
        X = f.read()
        thing_dic = json.loads(X)
        f.close()
    return thing_dic


def createC1(dataSet):
    '''
    生成C1
    :param dataSet:
    :return:
    '''
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    #将项集列表转换为不可变集和
    return [frozenset(item) for item in C1]

def scanD(D, Ck, minSupport = 50):
    '''
    扫描事务集D过滤Ck
    :param D:
    :param Ck:
    :param minSupport:
    :return:
    '''
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt.keys() : ssCnt[can] = 1
                else: ssCnt[can] += 1

    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):
    '''
    生成Ck
    :param Lk:
    :param k:
    :return:
    '''
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet, minSupport = 50):
    C1 = createC1(dataSet=dataSet)
    D = [set(item) for item in dataSet]
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        if len(Lk) > 0:
            L.append(Lk)
        else:
            break
        k += 1
        # print(k-1, "items", Lk)
    return L, supportData


if __name__ == "__main__":
    # dataSet, dataMap = loadDataSet()
    dataSet = loadDataSet()
    start = time.time()
    L, suppData = apriori(dataSet, minSupport=2)
    end = time.time()
    cnt = 1
    for i in L:
        print(cnt, i)
        cnt += 1
    print('Apriori total time:', end-start, 's')



