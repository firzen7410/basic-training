
def test():
    for i in range(1024):
        yield i
g=test()
print(next(g))
print(next(g))
print(next(g))
print(next(g))

