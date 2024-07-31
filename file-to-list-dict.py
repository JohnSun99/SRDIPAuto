lines = [line.rstrip('\n') for line in open('D:/eBook/Python/scripts/dcnDIP/AllDCNLeaf.csv')]
print(lines)

d = {}
with open("D:/eBook/Python/scripts/dcnDIP/AllDCNLeaf.csv") as f:
    for line in f:
       (key, val) = line.split(';')
       d[key] = val.rstrip('\n')

print("======== dictionary =============")
print(d)
