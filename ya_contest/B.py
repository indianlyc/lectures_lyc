n, m = map(int, input().split())
k = max(len(str(n - 1)), len(str(m - 1)))
a = [0] * k
res = 0
for i in range(n):
    s = i
    for j in range(k-1, -1, -1):
        a[j] = s // 10**j
        s = s % 10**j

    tt = 0
    for j in range(k-1, -1, -1):
        tt += a[j] * 10**(k-j-1)
    if tt < m:
        print("+", a, tt)
        res += 1
    else:
        print("-", a, tt)
print(res)