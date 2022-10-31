"""
Given whole numbers 1 <= n <= 10**18 and 2 <= m <= 10**5.
Find the remainder of the division nth Fibonacci nunber on m.
Time limit - 3 seconds.
Memory limit - 256 MB.
"""
def get_period(m):
    x, y = 0, 1
    period = 0
    while True:
        x, y = y, (x + y) % m
        period += 1
        if x == 0 and y == 1:
            return period


def fib_mod(n, m):
    period = get_period(m)
    if n % period == 0:
        return 0
    if n % period == 1:
        return 1
    x, y = 0, 1
    for _ in range(2, n % period + 1):
        x, y = y, (x + y) % m
    return y


def main():
    n, m = map(int, input().split())
    print(fib_mod(n, m))


if __name__ == "__main__":
    main()
