import copy

# 1. 建立 List
print("\n=== 建立List ===")
l = [2, 2, 5, 21, 3, 1, 35, 4, 6]
print("原始 l =", l)


# 1.中括號、list()、split()
# list()    只要是iterable的物件都可以轉成list
class student():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __iter__(self):
        return iter((self.name, self.age))


jack = student("jack", 25)
# list()做的事就相當於，利用iterator將物件內的元素append到list
temList = []
for i in jack:
    temList.append(i)
print(temList)
print(list(jack))
tuple_data = ('hello', 'world')
print("Tuple 轉 list:", list(tuple_data))
# split()
str1 = "he ll o wor ld!"
print("字串轉 list:", list(str1))  # 轉成字元 list

# split
print("字串使用 split:", str1.split())  # 預設依空白切分

# 2.特性
print("\n=== 特性 ===")
# 可變
# 可包含重複元素
# 有順序
# 可放入任何型別的元素
l.append("hello")
l.append({"jack": "pwd"})
l.append((1, 3, 5, [2, 4, 6]))
l.append({9, 8, 7})
print("l = ", l)

# 3.常用操作與方法
print("\n=== 常用操作與方法 ===")
# 新增
# append
# extend
l.extend([9, 8, 7])
print("after extend", l)
# insert
l.insert(0, "insert")
print("after insert :", l)

# 刪除
# del
del l[0]
print("del l1[0]:", l)

# remove(刪除index由小到大，第一個找到的value)
l.remove(2)
print("remove(2):", l)

# pop
print("pop(3) ->", l.pop(3))
print("pop 後:", l)

# 更新
l[2] = "update"

# 遍歷(iteration)
# for loop
for item in l:
    print(item)
# 取索引與值
for idx, val in enumerate(l):
    print(f"{idx}: {val}")

# 查詢
# in
print("查詢 l 是否包含 Hello :", "hello" in l)
# index
print("查詢值為hello的index在哪裡：", l.index("hello"))

# 其他常用
# sort
# 混合型別必須用key指定比較依據，key = str，將每個字元轉成string，按照字串的字母順序(ascii code)排序
l.sort(key=str)
print("sort:", l)

# len
print("l1的長度 = ", len(l))

# count
print("使用count(4)找出4出現的次數", l.count(4))

# join
# 元素必須全為string
l = ["hello", "world", "pwd"]
print("l = ", l)
print("使用join接起list內的所有項目，變成一個字串，要用一個字串插在連接的中間:", ','.join(l))

# map
# 語法:map(function, object)，對iterable物件(不是list專屬)內每一個元素執行function，回傳一個map物件，iterable，所以可以用List()轉成list，或者for loop遍歷
l=[1,2,3,4,5,6]

def square(num):
    return num ** 2
print("使用map平方",list(map(square, l)))

#filter
#語法:filter(function, object)，function必須回傳boolean value，以判斷物件內元素是否篩選掉，true留下，false離開
def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False
print("使用filter篩選偶數",list(filter(isEven, l)))

# 4. offset & slice
# offset
print("\n === offset & slice ===")
l2 = [12, "jonny", 43, "jack", 70, 81, 99, 0, 3]
print("\n原始l2:", l2)
print("l2 前 4 個元素（正向索引）:")
for i in range(4):
    print(l2[i], end=" ")

print("\n最後三個元素（負向索引）:")
for i in range(-1, -4, -1):
    print(l2[i], end=" ")

# slice 格式:l[start:stop:step]，如果step>0，start預設為1，stop為-1；如果step<0，start預設為-1，stop為-len(list)-1
print("\nslice範例:")
print("l2[2:7:2] ->", l2[2:7:2])
print("l2[::-2] (反向每隔 2 個取一個) ->", l2[::-2])
print("l2[:3:-1]", l2[:3:-1])

# slice賦值
l2[2:5] = "apple"
print("slice賦值後:", l2)

# 5.comprehension
# list comprehension的語法是由數學上用來建構集合的set-builder表達式所衍伸而來
# 而set-builder表達式最明顯的特徵就是頭尾的兩個大括號(curly brackets)所組成，在兩個大括號之間指明變數(variable)和條件(condiction)，就可以描述一個集合了
# 使用list comprehension的程式運作效率會比使用for loop及list的append()函式來得好，
# 因為list comprehension會使用更低階的bytecode指令來建造新的list，而for loop版本的append()函式呼叫會花費更高的計算成本
# 在某種程度上，list comprehension的功能就像是map()和filter()函式的綜合體，可以在一個表達式中同時完成map()及filter()函式的功能。
# 語法:[ 表達式 for 變數 in 可迭代物件 if 條件判斷式 ]
print("\n=== list comprehension ===")
l3 = [11, 4, 30, 7, 5, 0, 9, 15]
print("原始l3:",l3)
print("篩選偶數element:",[x for x in l3 if x % 2 == 0])

# 使用list comprehension 產生巢狀list
print("巢狀:",[(i, j) for i in range(4) for j in range(4)])

def qsort(A):
    if (A == []):
        return A
    pivot = A[0]
    return qsort([x for x in A[1:] if x < pivot]) + [pivot] + qsort([x for x in A[1:] if x >= pivot])
print("after qsort:",qsort(l3))

# 5. 複製方式比較
print("\n=== 複製方式比較 ===")

# 直接指派（共用同一個物件）
a = [1, 2, 3]
b = a
a[1] = 99
print("直接指派：a =", a, "b =", b, "(共用同一address)")

# slice建立新 List
c = a[:]
a[1] = 2
print("slice複製：a =", a, "c =", c, "(不同address)")

# copy()
d = a.copy()
a[1] = 97
print("copy()複製:a = ", a, "d =", d, "(不同address)")

# deepcopy
a = [0, 1, 2, 3, 4, [100, 200]]
print("\n原始 a=", a)
b = a[:]
a[5][0] = 777
print("slice複製： a=", a, "b=", b, "(a是巢狀結構，新複製的外層list會指向同一個內層list)")
c = copy.deepcopy(a)
a[5][0] = 123
print("deepcopy： a=", a, "c=", c, "(使用deepcopy完全複製內外層物件)")


