#1. 建立
# 字面量建立
dict1 = {"name": "Alice", "age": 25}

# 使用 dict() 建構函數
dict2 = dict(name="Bob", age=30)

# 從 list of tuples 建立
dict3 = dict([("name", "Charlie"), ("age", 28)])

# 使用 comprehension
dict4 = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4, 3:9, 4:16}

# 從兩個 list 配對建立
keys = ["a", "b", "c"]
values = [1, 2, 3]
dict5 = dict(zip(keys, values))

# 2. 特性
#可變
#不可包含重複key，如果出現，後面的會覆蓋前面的
#無序
#元素型別限制，key必須為可hash，如int,string,tuple，value可為任意型別
person= {"name": "Alice", "age": 25, 'gender': 'female'}

# 3.常見操作與方法
# 新增/更新
person['city'] = 'taipei'
person['age'] = 27

# 刪除
del person["city"]
person.pop("age")          # 會回傳刪除的值
person.popitem()           # 隨機刪除一組（3.7+ 為刪最後一組）

# 存取元素
print(person["name"])      # 直接取值（Key 不存在會報錯）
print(person.get("city"))  # 安全取值（Key 不存在回傳 None 或預設值）

# 遍歷
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(key, value)

# 查詢與檢測
print("name" in person)    # True
print("city" not in person)  # True

# 其他常用方法
person.update({"email": "alice@example.com"})
person.clear()             # 清空字典

# 4. comprehension
#語法:{key:value for item in iterable if condiction}
scores = {"Alice": 85, "Bob": 72, "Charlie": 90}
print(tuple(k for k in scores))

#zip
# 將多個可迭代物件一一配對
scores2 = {"Alice1": 850, "Bob2": 720, "Charlie3": 900}
print(list(zip(scores.keys(), scores2.values())))

