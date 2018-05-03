import numpy as np
import json

X = np.loadtxt("raw/Groceries.txt", delimiter='\\', dtype=np.str)[1:, 1]

data_set = []

int_data_set = []

for i in range(len(X)):
    arr = X[i].split(',')
    data_set.extend(arr)
    int_data_set.append(arr)


data_set = set(data_set)

thing_to_int = dict([(j, i) for (i, j) in enumerate(data_set)])
int_to_thing = dict([(i, j) for (i, j) in enumerate(data_set)])

thing_json = json.dumps(int_to_thing)
print(thing_json)
with open('data/Groceries_to_int.txt', 'w') as f:
    print(thing_json, file=f)
    f.close()

with open('data/Groceries.txt', 'w') as f:
    for i in range(len(int_data_set)):
        # tmpstr = ''
        for j in range(len(int_data_set[i])):
            int_data_set[i][j] = thing_to_int[int_data_set[i][j]]
        #     tmpstr += str(int_data_set[i][j]) + " "
        # print(tmpstr, file=f)

    # print(int_data_set, file=f)

    int_data_set = json.dumps(int_data_set)
    print(int_data_set, file=f)

    f.close()