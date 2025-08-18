def test(**d):
    for k, v in d.items():
        print(k, v)


s = {'a': 1, 'c': 3, 'd': 4, 'b': 2}
test(**s)
