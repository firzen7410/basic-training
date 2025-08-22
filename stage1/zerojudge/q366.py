N, M, Q = map(int, input().split())
sit_table=[]
sit_dict = {}
for i in range(N):
    a = list(map(int,input().split()))
    sit_table.append(a)
    for j,num in enumerate(a):
        sit_dict[num] = (i,j)

stand=[]
for _ in range(Q):
    draw = int(input())
    i, j = sit_dict[draw]
    # 取出上面
    if i-1 < 0:
        stand.append(sit_table[N-1][j])
    else:
        stand.append(sit_table[i-1][j])
    #取出下面
    stand.append(sit_table[(i+1)%N][j])
    #取出左邊
    if j-1 < 0:
        stand.append(sit_table[i][M-1])
    else:
        stand.append(sit_table[i][j-1])
    # 取出右邊
    stand.append(sit_table[i][(j+1)%M])
    stand.sort()
    print(*stand)
    stand.clear()




