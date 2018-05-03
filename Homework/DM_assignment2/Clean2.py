import json

with open('raw/sanitized_all.981115184025', 'r') as f:
    X = f.read()
    f.close()
X = X.lstrip("**SOF**")
X = X.rstrip("**EOF**\n")
X = X.split("**EOF**\n**SOF**")
# print(X)

data_set = []

int_data_set = []


for i in range(len(X)):
    X[i] = X[i][1:-1]
    # X[i] = X[i].rstrip('\\n')
    data_set.extend(X[i].split('\n'))
    int_data_set.append(X[i].split('\n'))

data_set = set(data_set)

print(data_set)


thing_to_int = dict([(j, i) for (i, j) in enumerate(data_set)])
int_to_thing = dict([(i, j) for (i, j) in enumerate(data_set)])

thing_json = json.dumps(int_to_thing)
print(thing_json)
with open('data/Unix0_to_int.txt', 'w') as f:
    print(thing_json, file=f)
    f.close()

with open('data/Unix0.txt', 'w') as f:
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