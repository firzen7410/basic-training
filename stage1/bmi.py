import sys


def calc_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python bmi.py <weight_kg> <height_m>")
    else:
        print(sys.argv[0])
        weight = float(sys.argv[1])
        height = float(sys.argv[2])
        print("Your BMI is:", calc_bmi(weight, height))
