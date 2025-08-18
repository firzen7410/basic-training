muti=[["Medium Wac",4],["WChicken Nugget",8],["Geez Burger",7],["ButtMilk Crispy Chicken",6],["Plastic Toy",3]]
single=[["German Fries",2],["Durian Slices",3],["WcFurry",5],["Chocolate Sunday",7]]

total = 0
while True:
    instr = int(input())
    if instr == 0:
        print("Total:",total)
        break
    order = int(input())
    if instr == 1:
        print(muti[order-1][0],muti[order-1][1])
        total += muti[order-1][1]
    elif instr == 2:
        print(single[order-1][0],single[order-1][1])
        total += single[order-1][1]

