array = [
    [1.00, 1.45, 0.52, 0.72],
    [0.70, 1.00, 0.31, 0.48],
    [1.95, 3.10, 1.00, 1.49],
    [1.34, 1.98, 0.64, 1.00]
]

n = 4 # size length of matrix
p = 3 # main currency index

f = []
g = []
for i in range(n):
    f.append([0] * (1<<n)) # f: n by 2^n
    g.append([0] * (1<<n)) 

for s in range(1<<n):
    if s == (1<<p):
        f[p][s] = 1
        continue
    if (s>>p)&1 == 0:
        continue
    for i in range(n):
        if (s>>i)&1 == 0:
            continue
        for j in range(n):
            if (s>>j)&1 == 0 or i==j:
                continue
            if f[i][s] < f[j][s-(1<<i)]*array[j][i]:
                f[i][s] = f[j][s-(1<<i)]*array[j][i]
                g[i][s] = j
            

mx = 0

for s in range(1<<n):
    for i in range(n):
        if (s>>i)&1:
            mx = max(mx, f[i][s] * array[i][p])

for s in range(1<<n):
    for i in range(n):
        if (s>>i)&1 and f[i][s] * array[i][p] == mx and mx>1:
            print(f"This is the way that has {f[i][s]*array[i][p]}")
            x = i
            t = s
            while t:
                print(f"{x}")
                x,t = g[x][t], t - (1<<x)

