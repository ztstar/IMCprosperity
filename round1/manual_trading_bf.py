array = [
    [1.00, 1.45, 0.52, 0.72],
    [0.70, 1.00, 0.31, 0.48],
    [1.95, 3.10, 1.00, 1.49],
    [1.34, 1.98, 0.64, 1.00]
]

mx = 0
p = 3

for i in range(4):
    for j in range(4):
        for k in range(4):
            for r in range(4):
                mx = max(mx, array[p][i]*array[i][j]*array[j][k]*array[k][r]*array[r][p])

flag = False

for i in range(4):
    for j in range(4):
        for k in range(4):
            for r in range(4):
                if mx == array[p][i]*array[i][j]*array[j][k]*array[k][r]*array[r][p]:
                    print(f"Optimal strategy with {i},{j},{k},{r} that results in {mx}")
                    flag = True
                    break
            if flag:
                break
        if flag:
            break
    if flag:
        break