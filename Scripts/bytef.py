import pickle as pic
f = open("Base.txt", "r")
n = 0
w = {}
keys = ['name', 'year', 'dev', 'mass', 'efmass', 'stages']
for string in f:
    string = string.rstrip()
    a = string.split()
    print(a)
    w[str(n)] = {'name':a[0], 'year':a[1], 'dev':a[2], 'mass':a[3], 'efmass':a[4], 'stages':a[5]}
    n += 1
k = open("Rick.pic", "wb")
pic.dump(w, k)
f.close()
k.close()
