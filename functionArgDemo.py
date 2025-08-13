def score(eg_score, math_score, el_weight, math_weight):
    return eg_score * el_weight + math_score * math_weight


# positional argument
print(score(70, 60, 0.5, 0.5))

# keyword argument
print(score(math_score=70, el_weight=0.5, math_weight=0.5, eg_score=60))

def fun(a, b, c=10, d=20):
    return a + b + c + d
print(fun(3, 4))

# 必要參數要放在有預設值參數的前面
# def fun(a=10, b=20, c, d) >> syntax error

# 位置參數必須放在關鍵字參數前面
# print(fun(a=10,b=20,30,40)) >> syntax error

# unpacking參數 * 與 **
#傳入時拆包
a = [2,3]
b = {'c':4,'d':5}
print(fun(*a,**b))

# 接收時拆包，函式在接收時會打包成tuple
def sum_numbers(*args):
    print(type(args))
    total = 0
    for num in args:
        total += num
    return total
print(sum_numbers(1,2,3))

def show(**args):
    for key, value in args.items():
        print(key, value)
show(name='jack',age='29')
