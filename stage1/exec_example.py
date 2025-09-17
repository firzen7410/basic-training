# 比較step into &step over
<<<<<<< HEAD
=======
x = 10


>>>>>>> 4f4dad3 ('重置')
def calculate(a1, a2) -> int:
    a = add(a1, a2)
    m = multiply(a1, a2)
    s = a + m
    return s


def add(a1, a2):
    return a1 + a2


def multiply(a1, a2):
    return a1 * a2


for i in range(10):
    print(calculate(i, i + 1))
calculate(multiply(2, 3), add(3, 4))
