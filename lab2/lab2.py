import numpy as np
class Node():
    def __init__(self, name = "", children = [], costs = 0, profit = 0, n = 0, p = 0, selectOption = False):
        self.name = name
        self.children = children
        self.costs = costs
        self.profit = profit
        self.n = n
        self.p = p
        self.selectOption = selectOption

    def selectBestOption(self):
        if len(self.children) == 0:
            self.value = self.p * (self.profit * self.n - self.costs)
        else:
            [x.selectBestOption() for x in self.children]
            if self.selectOption:
                self.best = max(self.children)
                self.value = self.best.value
            else:
                self.value = sum([x.value for x in self.children])

    def __gt__(self, other):
        return self.value > other.value

    def addChild(self, name = "", children = [], profit = 0, p = 0, selectOption = False):
        self.children.append(Node(name = name, children = children, profit = profit, selectOption = selectOption, n = self.n, p = p, costs = self.costs))

    def clearChildren(self):
        self.children = []
        self.value = None
        self.best = None

    def describe(self, short = True):
        print(f'Назва: {self.name}')
        if self.value:
            print(f'При цьому варіанті розвитку подій прибуток складатиме {self.value}')
        if self.p and not short:
            print(f'Шанс виникнення: {self.p}')
        if self.costs and not short:
            print(f'Витрати: {self.costs}')
        if self.profit and not short:
            print(f'Річний прибуток: {self.profit}')
        if self.n and not short:
            print(f'Тривалість: {self.n} років')
        print()


    def summary(self):
        print(f'Дерево складається з {len(self.children)} вузлів.')
        if self.value and self.best:
            print("Рішення знайдено:")
            self.best.describe()
        else:
            print("Рішення ще не знайдено")
        print()
        print("Опис вузлів дерева:")
        [x.describe(False) for x in self.children]


values = np.genfromtxt("Kruvui\\lab2\\lab2_data.csv",delimiter=',')
def buildFactory(p1 = values[2], p2 = values[4], n = 5):
    case_A = Node(name = "Побудова великого заводу", costs = values[0], n = n)
    case_A.clearChildren()
    case_A.addChild(name = "Успіх", profit = values[1], p = p1)
    case_A.addChild(name = "Невдача", profit = values[3], p = p2)

    case_B = Node(name = "Побудова малого заводу", costs = values[5], n = n)
    case_B.clearChildren()
    case_B.addChild(name = "Успіх", profit = values[6], p = p1)
    case_B.addChild(name = "Невдача", profit = values[8], p = p2)
    return [case_A, case_B]

[case_A, case_B] = buildFactory()
case_C = Node(name = "Дослідження")
case_C.clearChildren()
case_C.addChild(name = "Успіх", profit = 0, p = values[11], selectOption = True, children = buildFactory(values[12],values[13], 4))
case_C.addChild(name = "Невдача", profit = 0, p = values[11])

tree = Node(name = "Рішення", children = [case_A, case_B, case_C], selectOption = True)
tree.selectBestOption()
tree.summary()
