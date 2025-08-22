def test():
    for i in range(10):
        yield i


a = test()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
