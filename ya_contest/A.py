N = int(input())
a = list(map(int, input().strip().split()))

if N % 2 == 1:
    print(-1)
else:
    b = list(map(sum, zip(a[:N // 2], a[N // 2:][::-1])))
    b = sorted(b)

    if b[0] == b[-1]:
        print(b[0])
    else:
        print(-1)