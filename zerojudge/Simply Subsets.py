import sys
A = set()
B = set()
cnt = 0
for line in sys.stdin:
    cnt+=1
    line = line.strip()
    if(cnt == 1):
        for num in line.split():
            A.add(int(num))
    else:
        for num in line.split():
            B.add(int(num))

    if(cnt == 2):
        if(A & B == A & B & A == B):
            print("A equals B")
        elif(A & B == A & B & A == A):
            print("A is a proper subset of B")
        elif(A & B == B & B & A == B):
            print("B is a proper subset of A")
        elif(not A & B):
            print("A and B are disjoint")
        elif(A & B == B & A):
            print("I\'m confused!") 
        cnt = 0
        A=set()
        B=set()
    