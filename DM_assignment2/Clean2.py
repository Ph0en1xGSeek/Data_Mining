

with open('raw/sanitized_all.981115184025', 'r') as f:
    X = f.read()
    f.close()
X = X.lstrip("**SOF**")
X = X.rstrip("**EOF**\n")
X = X.split("**EOF**\n**SOF**")
print(X)

dataSet = []

for i in range(len(X)):
    X[i] = X[i][2:-2]
    # X[i] = X[i].rstrip('\\n')
    dataSet.append(X[i].split('\\n'))

print(X[i])