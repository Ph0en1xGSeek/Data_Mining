import Apriori
import FPgrowth
import time
import matplotlib.pyplot as plt
import numpy as np

# time1 = []
# time2 = []
num_set = []
dataSet = Apriori.loadDataSet()
initSet = FPgrowth.createInitSet(dataSet)
iter = 1
x = range(100, 0, -10)

for minSup in range(100, 0, -10):

    # start = time.time()
    # L, suppData = Apriori.apriori(dataSet, minSupport=minSup)
    # end = time.time()
    # cnt = 1
    # for i in L:
    #     # print(cnt, i)
    #     cnt += 1
    # print(iter, ':Apriori total time:', end-start, 's')
    # time1.append(end-start)

    start = time.time()
    # 建好FP树
    FPTree, HeaderTab = FPgrowth.createTree(initSet, minSup=minSup)
    freqItems = []
    # 根据每个结点挖掘频繁项集
    FPgrowth.mineTree(FPTree, HeaderTab, minSup=minSup, preFix=set([]), freqItemList=freqItems)
    end = time.time()
    # print(freqItems)
    print(iter, ":FP-Growth total time:", end-start, 's')
    # time2.append(end-start)
    num_set.append(len(freqItems))
    iter += 1

plt.plot(x, num_set, label='FP-growth', color='b')
plt.xlabel('minSupport')
plt.ylabel('Number of ItemSets')
plt.title('number of ItemSets')
plt.legend()
plt.show()
plt.close()
print(num_set)
#
# plt.plot(x, time1, label='Apriori', color='r')
# plt.plot(x, time2, label='FP-growth', color='b')
# plt.xlabel('minSupport')
# plt.ylabel('time(second)')
# plt.title('Apriori & FP-growth')
# plt.legend()
# plt.show()
# plt.close()
#
# plt.plot(x, time1, label='Apriori', color='r')
# plt.xlabel('minSupport')
# plt.ylabel('time(second)')
# plt.title('Apriori')
# plt.legend()
# plt.show()
# plt.close()
#
# plt.plot(x, time2, label='FP-growth', color='b')
# plt.xlabel('minSupport')
# plt.ylabel('time(second)')
# plt.title('FP-growth')
# plt.legend()
# plt.show()
# plt.close()



# x = range(10)
# y = [1,2,3,5,4,8,3,8,1,15]
#
# plt.plot(x, y)
# plt.show()