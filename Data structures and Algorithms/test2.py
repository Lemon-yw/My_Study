def test(A, B, mod):
    res = float('inf')
    for x in A:
        for y in B:
            temp2 = (x + y) % mod
            if temp2 < res:
                res = temp2
    return res


if __name__ == '__main__':
    n, m, mod = map(int, input().strip().split())
    A = [i for i in map(int, input().strip().split())]
    B = [i for i in map(int, input().strip().split())]
    print(test(A, B, mod))
