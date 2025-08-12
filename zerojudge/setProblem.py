# 在班上，總是會有那麼一兩個同學特別愛說別人閒話。有一天，愛八卦的同學想要知道班上的小團體到底有幾個，他知道班上誰跟誰是朋友，但是因為愛八卦的同學很懶，所以他委託你寫一個程式幫他把小團體的數目計算出來。
#
# 輸入說明
# 多筆測資
#
# 每筆測資第一行會有二個正整數
# n, k(int)
#
# n代表班上的人數(編號為0~n - 1)，k是接下來有幾筆關係
#
# 再來有k行，每行有二個整數
# a, b
# 代表編號
# a
# 跟
# b
# 的人是朋友
#
# 輸出說明
# 輸出總共有幾個小團體
#
# 小團體的定義是你的朋友或者是朋友的朋友跟你屬於同一個小團體
# 範例輸入 #1
# 5 6
# 1 0
# 0 1
# 1 2
# 2 3
# 2 4
# 4 1
# 5 4
# 1 0
# 0 1
# 2 3
# 2 4
# 範例輸出 #1
# 1
# 2

import io, sys
sys.stdin = io.StringIO("""
6 5
0 3
5 4
5 3
2 1
0 5
""")
data = sys.stdin.read().strip().split("\n")
i = 0
tmpSet=set()
circle = []
while i < len(data):
    n, k = map(int, data[i].split())
    i += 1

    for _ in range(k):
        isNeedNew = 0
        a, b = map(int, data[i].split())
        if not tmpSet:
            tmpSet.add(a)
            tmpSet.add(b)
            isNeedNew = 1
        else:
            for x in circle:
                if a in x or b in x:
                    x.add(a)
                    x.add(b)
                    isNeedNew = 0
                    break
                else:
                    isNeedNew = 1
                    tmpSet.clear()
                    tmpSet.add(a)
                    tmpSet.add(b)
        if isNeedNew:
            circle.append(tmpSet.copy())
        i+=1

print(circle)

#check merge
for x in circle:
    for y in circle:
        if x != y and (x & y) :
            for element in x:
                element.add(y)

