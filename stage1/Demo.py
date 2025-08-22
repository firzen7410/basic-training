def test(**d):
    for k, v in d.items():
        print(k, v)


s = {'a': 1, 'c': 3, 'd': 4, 'b': 2}
test(**s)

l = [23, 4, 5, 6, 2, 4, 6, 12]
l.index(99)

test({'jack': 22, 'mark': 34})
