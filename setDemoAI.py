"""
Demo: Python set 資料結構
依大綱結構展示：
1. 建立方式
2. 特性
3. 常用操作
4. 不支援索引與切片
5. 推導式
6. 典型應用
7. 注意事項
"""

# 1. 建立方式 (Creation)
print("=== 1. 建立方式 ===")
set_a = {1, 2, 3}               # 字面量建立
set_b = set([3, 4, 5])          # 用 set() 轉換可迭代物件
set_c = set()                   # 空集合必須用 set()，不能用 {} (會變成 dict)
print(set_a, set_b, set_c)

# 2. 特性 (Properties)
print("\n=== 2. 特性 ===")
print("是否可變:", "可變 (mutable)")
print("是否允許重複元素:", "否，會自動去重")
set_d = {1, 2, 2, 3, 3}
print("自動去重後:", set_d)
print("是否有順序:", "無序 (unordered) → 印出順序可能不同")
print("元素型別限制:", "必須是可 hash，不可包含 list、dict")

# 3. 常用操作 (Common Operations)
print("\n=== 3. 常用操作 ===")
my_set = {1, 2, 3}
my_set.add(4)        # 新增
print("新增 4:", my_set)
my_set.remove(2)     # 刪除 (若不存在會報錯)
print("刪除 2:", my_set)
my_set.discard(99)   # 刪除，不存在也不報錯
print("discard 不存在元素:", my_set)
print("是否包含 3:", 3 in my_set)

# 集合運算
set_x = {1, 2, 3}
set_y = {3, 4, 5}
print("交集:", set_x & set_y)
print("聯集:", set_x | set_y)
print("差集:", set_x - set_y)
print("對稱差集:", set_x ^ set_y)

# 4. 不支援索引與切片
print("\n=== 4. 不支援索引與切片 ===")
try:
    print(my_set[0])
except TypeError as e:
    print("錯誤:", e)

# 5. 推導式 (Comprehension)
print("\n=== 5. 推導式 ===")
squares = {x**2 for x in range(5)}
print("平方集合:", squares)

# 6. 典型應用場景
print("\n=== 6. 典型應用 ===")
data = [1, 2, 2, 3, 4, 4, 5]
unique_data = set(data)    # 快速去重
print("原始資料:", data)
print("去重後:", unique_data)

# 7. 注意事項與陷阱
print("\n=== 7. 注意事項 ===")
try:
    invalid_set = {1, [2, 3]}  # list 是不可 hash，會報錯
except TypeError as e:
    print("錯誤:", e)

# tuple 可放進 set，但若 tuple 裡包含 list 仍會報錯
valid_set = {(1, 2), (3, 4)}
print("tuple 當元素:", valid_set)
