
def testYield():
    for i in range(1024):
        yield i
g=testYield()
print(next(g))
print(next(g))
print(next(g))
print(next(g))

def testReturn():
    for i in range(1024):
        return i

s = testReturn()
print(s)

def echo():
    received = yield "Start"
    while True:
        received = yield received
gen = echo()
print(next(gen))
print(gen.send("第一"))