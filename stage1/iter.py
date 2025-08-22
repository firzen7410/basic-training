nums = [10, 20, 30]
it = iter(nums)  # 建立迭代器

print(dir(it))
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
