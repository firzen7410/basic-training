# module_a.py
def hello():
    print("Hello from module_a!")
class Greeter:
    def hello(self):
        print("Hello from module_a!")

if __name__ == '__main__':
    print("module_a.py 被直接執行")
    greeter = Greeter()
    greeter.hello()
