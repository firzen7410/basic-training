# 比較step into &step over
def calculate(a1, a2) -> int:
    a = add(a1, a2)
    m = multiply(a1, a2)
    s = a + m
    return s


def add(a1, a2):
    return a1 + a2


def multiply(a1, a2):
    return a1 * a2


x = 3
y = 4
print(calculate(x, y))
