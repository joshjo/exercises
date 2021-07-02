import sys


map = {
    1: 2,
    2: 2,
    3: 3,
}


def fibo3_recursive(x):
    if x in map:
        return map[x]
    if x < 3:
        return 2
    if x == 3:
        return 3
    result = fibo3_recursive(x - 1) + fibo3_recursive(x - 2) + fibo3_recursive(x - 3)
    map[x] = result
    return result


def fibo3_iterative(x):
    a, b, c = 2, 2, 3
    for _ in range(1, x):
        a, b, c = b, c, a + b + c
    return a


if __name__ == '__main__':
    args = len(sys.argv)
    if args != 2:
        print('Invalid arguments size')
    value = int(sys.argv[1])
    print(fibo3_iterative(value))
