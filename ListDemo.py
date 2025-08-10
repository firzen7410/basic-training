"""
1. 建立 List
2. 使用split或list()轉成List
3. 合併與extend
4. offset與slice
5. 複製方式比較
6. 常用方法
7. list comprehension
"""
import copy

# ================================
# 1. 建立 List
# ================================
l = [2, 5, 21, 3, 1, 35, 4, 6]
print("原始 l =", l)

# ================================
# 2. 使用split或list()轉成List
# ================================
#List()
str1 = "he ll o wor ld!"
class student():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __iter__(self):
        return iter((self.name,self.age))
jack = student("jack", 25)
l=[]
for i in jack:
   l.append(i)
print(l)
print(list(jack))
print("字串轉 list:", list(str1))  # 轉成字元 list

#split
print("\n字串使用 split:", str1.split())  # 預設依空白切分

tuple_data = ('hello', 'world')
print("Tuple 轉 list:", list(tuple_data))

# ================================
# 3. 合併與extend
# ================================
l1 = [8, 11, 3, 1]
l2 = [21, 3, 4, 5, 9, 14, 27]

print("\n使用 + 合併:", l1 + l2)
l1.extend(l2)  # 會改到l1
print("使用 extend 後:", l1)

# ================================
# 4. offset & slice
# ================================
print("\n原始l2:", l2)
print("l2 前 4 個元素（正向索引）:")
for i in range(4):
    print(l2[i], end=" ")

print("\n最後三個元素（負向索引）:")
for i in range(-1, -4, -1):
    print(l2[i], end=" ")

print("\nslice範例:")
#格式:l[start:stop:step]，如果step>0，start預設為1，stop為-1；如果step<0，start預設為-1，stop為-len(list)-1
print("l2[2:7:2] ->", l2[2:7:2])
print("l2[::-2] (反向每隔 2 個取一個) ->", l2[::-2])
print("l2[:3:-1]",l2[:3:-1])

# slice賦值（可用任何 iterable 取代）
l2[2:5] = "apple"
print("slice賦值後:", l2)

# ================================
# 5. 複製方式比較
# ================================
print("\n=== 複製方式比較 ===")

# 直接指派（共用同一個物件）
a = [1, 2, 3]
b = a
a[1] = 99
print("直接指派：a =", a, "b =", b, "(共用同一address)")

# slice建立新 List
c=a[:]
a[1] = 2
print("slice複製：a =", a, "c =", c, "(不同address)")

# copy()
d=a.copy()
a[1]=97
print("copy()複製:a = ",a,"d =",d,"(不同address)")

#deepcopy
a = [0, 1, 2, 3, 4, [100, 200]]
print("\n原始 a=",a)
b=a[:]
a[5][0] = 777
print("slice複製： a=",a,"b=",b,"(a是巢狀結構，新複製的外層list會指向同一個內層list)")
c= copy.deepcopy(a)
a[5][0] = 123
print("deepcopy： a=",a,"c=",c,"(使用deepcopy完全複製內外層物件)")

# ================================
# 6. 常用方法
# ================================
l1 = [1, 1, 4, 5, 1, 4]
print("\n=== 常用方法 ===")
print("原始 l1 =", l1)

#append
l1.append(2)
print("append(2):", l1)

#insert
l1.insert(2, 5)
print("insert(2, 5):", l1)

#del
del l1[0]
print("del l1[0]:", l1)

#remove
l1.remove(5)
print("remove(5):", l1)

#pop
print("pop(3) ->", l1.pop(3))
print("pop 後:", l1)

#sort
l1.sort(reverse=True)
print("sort(reverse=True):", l1)

#index
print("使用index找出值為2的index在哪裡：",l1.index(2))

#len
print("l1的長度 = ",len(l1))

#count
print("使用count(4)找出4出現的次數",l1.count(4))

#join
a=["hi","how are you","bye"]
print("使用join接起list內的所有項目，變成一個字串，要用一個字串插在連接的中間",','.join(a))

#in
a=["car","airplane","gas"]
print("使用 in 檢查a存不存在gas這個元素：","gas" in a)

# ================================
# 6. list comprehension
# ================================
# 更精簡、更有效率的方式從一個list，產生出另一個list

#語法：[output collection condiction]
print("\n=== list comprehension ===")
a=[1,2,3,4,5,6,7,8,9,10]
print("印出a的偶數項:",[x for x in a if x%2==0])