class People(object):
    def __init__(self, age):
        self._age = age
        self._sex = "Male"

    def getAge(self):
        return self._age

    def getSex(self):
        return self._sex


class Man(People):
    def __init__(self, age):
        People.__init__(self, age)

    def changeAge(self):
        self._age = 100

    def changeSex(self):
        self._sex = "Female"


class Boy(Man):
    def __init__(self, age):
        Man.__init__(self, age)

    def change(self):
        self._age = 1000

def main():
    p = Man(10)
    print(p.getSex())
    p.changeSex()
    print(p.getSex())


if __name__ == "__main__":
    main()