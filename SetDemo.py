# 集合
# 1. 如何建立
set1 = {7, 2, 7, 3, 4, 8}
set2 = set()

# 2. 特性
print('\n=== 特性 ===')
# 可變
# 無序
# 重複元素會被刪除
print('set1=', set1)
set1.add(10)
print(set1)

print('=== 元素型別限制 ===')
# 只要不可變&可被hash就可以放入set，像int, string, tuple(但如果包含list這種可變物件就無法加入)
temList = [9, 9, 9, 9, 10]
temTuple = (5, 3, 4, 1)
temSetF = frozenset({3, 5, 7, 9})
temTuple2 = ([5, 3, 43, 1], 0, 3)
temStr = "hello world"
temDict = {'jack': '114514'}
print("成功加入的例子")
try:
    set2.add(42)  # int
    set2.add(3.14)  # float
    set2.add(temStr)  # str
    set2.add(temTuple)  # tuple (無可變物件)
    set2.add(temSetF)
    print("set2:", set2)
except TypeError as e:
    print("錯誤:", e)

print("\n無法加入的例子")
examples = [temList, temTuple2, temDict]
for item in examples:
    try:
        set2.add(item)
    except TypeError as e:
        print(f"加入 {item} 失敗:", e)

# 3. 常用操作
print("\n=== 3. 常用操作 ===")
set1.add(4)  # 新增
print("新增 4:", set1)
set1.remove(2)  # 刪除 (若不存在會報錯)
print("刪除 2:", set1)
set1.discard(99)  # 刪除，不存在也不報錯
print("discard 不存在元素:", set1)
print("是否包含 3:", 3 in set1)

# 集合運算
set_x = {1, 2, 3}
set_y = {3, 4, 5}
print("交集:", set_x & set_y)
print("聯集:", set_x | set_y)
print("差集:", set_x - set_y)
print("對稱差集:", set_x ^ set_y)
