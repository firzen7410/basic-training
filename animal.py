# 動物類別
class Animal:
    def eat(self):
        pass

# 鳥類類別
class Bird(Animal):
    def eat(self):
        print("Bird fly method is called.")


# 鴨子類別
class Duck(Animal):
    def eat(self):
        print("Duck fly method is called.")


duck = Duck()
duck.eat()
