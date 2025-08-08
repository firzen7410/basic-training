# 集合
set1 = {7, 2, 7, 3, 4, 8}
set2 = {12, 34, 2, 1, 5, 7, 12}

# 重複元素會被刪除
print('set1=', set1)
print('set2=', set2)

# 元素個數
print('len(set1)=', len(set1))

# 加入(只要不可變&可被hash就可以放入set，像int, string, tuple(但如果包含list這種不可被hash的物件就無法加入)，)
l = [9, 9, 9, 9, 10]
temTuple = (5, 3, 4, 1)
temTuple2 = ({5, 3, 43, 1}, 0, 3)
str1 = "hello world"
temDict = {'jack': '114514'}


def hashTest(test):
    try:
        hash(test)
        print(test, 'is hashable');
    except(TypeError):
        print(test, 'TypeError occured');


hashTest(l)
hashTest(temTuple)
hashTest(temTuple2)
hashTest(str1)
hashTest(temDict)
set1.add(temTuple)
print('set1 after added:', set1)

# 刪除
try:
    set1.remove(1024)
except(KeyError):
    print('KeyError')
print(set1)
print(set2)

# 聯集
print('union:', set1.union(set2))

# 交集
print('intersection', set1.intersection(set2))
