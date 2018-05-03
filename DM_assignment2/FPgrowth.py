import json
import time

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        # 值
        self.name = nameValue
        # 计数
        self.count = numOccur
        # 下一个相同值的结点
        self.nodeLink = None
        # 父节点
        self.parent = parentNode
        # 孩子结点
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print(" "*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

def loadDataSet():
    thing_arr = []

    with open('data/Groceries.txt', 'r') as f:
        X = f.read()
        thing_arr = json.loads(X)
        f.close()
    return thing_arr
    # return [[1,2,5], [2,4], [2,3], [1,2,4],[1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]

def loadMap():

    thing_dic = {}
    with open('data/Groceries_to_int.txt', 'r') as f:
        X = f.read()
        thing_dic = json.loads(X)
        f.close()
    return thing_dic

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def createTree(dataSet, minSup = 1):
    '''
    创建根结点以及搜索链表表头
    :param dataSet:
    :param minSup:
    :return:
    '''

    # 搜索链表头
    headerTable = {}
    # 在搜索用的链表头除记录每个item的频数
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    # 小于最小支持度的item不用考虑
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    # 如果不存在频繁项集则直接返回空
    if len(freqItemSet) == 0:
        return None, None
    # 为每个结点增加一个指向下一个同值结点的指针
    for k in headerTable.keys():
        headerTable[k] = [headerTable[k], None]
    # 树根
    retTree = treeNode('Null Set', 1, None)

    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            # 每个transaction中的item按出现的次数从高到低排
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            # 建树
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    '''
    每个transaction递归更新到树上，并更新搜索链表
    :param items:
    :param inTree:
    :param headerTable:
    :param count: 每个transaction的出现次数
    :return:
    '''
    # 每个transaction的最高出现词数item直接接在root上
    if items[0] in inTree.children:
        # 有该元素项时计数值+1
        inTree.children[items[0]].inc(count)
    else:
        # 没有这个元素项时创建一个新节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    # 递归建树
    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
    '''
    找到链表尾加上一个
    :param nodeToTest:
    :param targetNode:
    :return:
    '''
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode, prefixPath):
    '''
    递归寻找父节点
    :param leafNode:
    :param prefixPath:
    :return:
    '''
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        # 获得某个叶子节点的前缀路径
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) >= 2:
            # 去掉自己获得前缀路径，且权重为当前结点的权重，用于建立条件前缀树
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    '''
    递归查找频繁项集
    :param inTree: FP树
    :param headerTable:
    :param minSup:
    :param preFix: 当前前缀
    :param freqItemList: 存储频繁项集
    :return:
    '''
    # 从出现次数少的开始找
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]

    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        CondTree, Header = createTree(condPattBases, minSup)

        if Header != None:
            mineTree(CondTree, Header, minSup, newFreqSet, freqItemList)




if __name__ == "__main__":

    minSup = 300
    dataSet = loadDataSet()
    dataMap = loadMap()
    initSet = createInitSet(dataSet)
    start = time.time()
    # 建好FP树
    FPTree, HeaderTab = createTree(initSet, minSup=minSup)
    freqItems = []
    # 根据每个结点挖掘频繁项集
    mineTree(FPTree, HeaderTab, minSup=minSup, preFix=set([]), freqItemList=freqItems)
    end = time.time()
    # print(freqItems)
    # print("FP-Growth total time:", end-start, 's')
    for itemSet in freqItems:
        if len(list(itemSet)) >= 2:
            output_str = ''
            for item in itemSet:
                output_str += dataMap[str(item)] + ' + '
            print(output_str)