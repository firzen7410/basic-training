# tuple

# 1. 建立
print("=== 建立tuple ===")
# 在項目後方加上逗號，使用逗號區隔兩個變數時，Python預設為元組(Tuple)資料型態
number = 6, 2, 0
print(number)
# 如果只有一個項目，後面一定要記得加逗號
number = 6,
print(number)

# 小括號
number = (1, 1, 4)
print(number)

# tuple()
str1 = "hello world"
print(tuple(str1))

# 2. 特性
print("\n=== 特性 ===")

# 可放入任何型別的元素
tuple1 = (4, 4, "hello", {6, 3, 4}, {"jack": "jack"}, (1, 7, (20, 1, 90), 0, 2), [72, 10, (1024, 90)])

# 不可變，但若元素包含可變元素，他們的內容一樣可修改
tuple1[6].append('hi')
print(tuple1)
# 有序(可被索引)
print(tuple1[0])
# 可包含重複元素

# 3.常用操作與方法
tuple2 = (0, 5, 1, 12, 7, 4, 1)
#slice
print(tuple2[1:5])

#unpacking
apple, *banana, orange = tuple2
print(apple,banana,orange)