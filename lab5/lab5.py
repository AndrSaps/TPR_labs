import numpy as np

class Matrix():
    """docstring for Matrix."""

    def __init__(self, values = []):
        self.values = values

    def find_point(self):
        max_win = [max(x) for x in self.values.T]
        min_lose = [min(x) for x in self.values]
        print(f'Мінімальни програш: {min_lose}\nМаксимальний виграш {max_win}')
        if max(max_win) != min(min_lose):
            print('Сідлової точки не існує. Рішень в чистих стратегіях не існує.')
        else:
            y = max(max_win)
            index_of_point = min_lose.index(y)
            x = self.values[index_of_point].index(x)
            print(f'Сідлова точка знайдена за координатами {x},{y}: {self.values[x][y]}')

    def optimal_strategy(self, p1 = None, p2 = None):
        if not p1:
            print(f'Оскільки змішана стратегія P1 першого гравця не задана, припустимо що шанси вибору всіх стратегій рівні.')
            p1 = np.full((1, len(self.values)), 1/len(self.values))
        if not p2:
            print(f'Оскільки змішана стратегія P2 другого гравця не задана, припустимо що шанси вибору всіх стратегій рівні.')
            p2 = np.full((1, len(self.values)), 1/len(self.values))
        optimal = np.dot(np.dot(p1, self.values), p2.T)
        print(f'При достатній кількості ігор середній виграш та середній програш гравців становить {optimal[0]}')

    def optimize(self):
        optimized_1 = [[np.all(x - y>=0)  for x in self.values].count(True) == 1 for y in self.values]
        optimized_1 = self.values[optimized_1]
        print(f'Оптимізована матриця для 1 гравця\n{optimized_1}')
        optimized_2 = [[np.all(x - y >=0)  for x in self.values.T].count(True) == 1 for y in self.values.T]
        optimized_2 = self.values.T[optimized_2].T
        print(f'Оптимізована матриця для 2 гравця\n{optimized_2}')
        return optimized_1

values = np.genfromtxt("Kruvui\\lab5\\lab5_data.csv",delimiter=',')
values
matrix = Matrix(values)

matrix.find_point()

matrix.optimal_strategy()

optimized = matrix.optimize()


class LinearModel:
    def __init__(self, A=np.empty([0, 0]), b=np.empty([0, 0]), c=np.empty([0, 0]), minmax="MAX"):
        self.A = A
        self.b = b
        self.c = c
        self.x = [float(0)] * len(c)
        self.minmax = minmax
        self.printIter = True
        self.optimalValue = None
        self.transform = False

    def addA(self, A): #витрати
        self.A = A

    def addB(self, b): #запаси
        self.b = b

    def addC(self, c): #цільова
        self.c = c
        self.transform = False

    def setPrintIter(self, printIter):
        self.printIter = printIter

    def printSoln(self):
        print("\nОтримані y: ")
        print(self.x)
        print("Значення цільової функції: ")
        print(self.optimalValue)
        print("Знайдений вектор ймовірності для першого гравця можна записати у вигляді:\n P(0.125,0,0,0.875,0)")
        print("Знайдений вектор ймовірності для другого гравця можна записати у вигляді:\n Q(0,",self.x[0],",",0,",",0,",",self.x[1],")")

    def printTableau(self, tableau):
        print("ind \t\t", end="")
        for j in range(0, len(c)):
            print("x_" + str(j), end="\t")
        for j in range(0, (len(tableau[0]) - len(c) - 2)):
            print("s_" + str(j), end="\t")

        print()
        for j in range(0, len(tableau)):
            for i in range(0, len(tableau[0])):
                if (not np.isnan(tableau[j, i])):
                    if (i == 0):
                        print(int(tableau[j, i]), end="\t")
                    else:
                        print(round(tableau[j, i], 2), end="\t")
                else:
                    print(end="\t")
            print()

    def getTableau(self):
        # починаємо роботу із tableau
        if (self.minmax == "MIN" and self.transform == False):
            self.c[0:len(c)] = -1 * self.c[0:len(c)]
            self.transform = True

        t1 = np.array([None, 0])
        numVar = len(self.c)
        numSlack = len(self.A)

        t1 = np.hstack(([None], [0], self.c, [0] * numSlack))

        basis = np.array([0] * numSlack)

        for i in range(0, len(basis)):
            basis[i] = numVar + i

        A = self.A

        if (not ((numSlack + numVar) == len(self.A[0]))):
            B = np.identity(numSlack)
            A = np.hstack((self.A, B))

        t2 = np.hstack((np.transpose([basis]), np.transpose([self.b]), A))

        tableau = np.vstack((t1, t2))

        tableau = np.array(tableau, dtype='float')

        return tableau

    def optimize(self):

        if (self.minmax == "MIN" and self.transform == False):
            for i in range(len(self.c)):
                self.c[i] = -1 * self.c[i]
                transform = True

        tableau = self.getTableau()
        # якщо базис не вимагається
        optimal = False
        #трекаємо ітерації для виводу
        iter = 1

        while (True):

            if (self.minmax == "MAX"):
                for profit in tableau[0, 2:]:
                    if profit > 0:
                        optimal = False
                        break
                    optimal = True
            else:
                for cost in tableau[0, 2:]:
                    if cost < 0:
                        optimal = False
                        break
                    optimal = True

            #якщо всі результати знаходяться у мінімальних витратах або максимальному заробітку
            if optimal == True:
                break

            # nth змінних входять у базис, враховуючи індексацію для tableau
            if (self.minmax == "MAX"):
                n = tableau[0, 2:].tolist().index(np.amax(tableau[0, 2:])) + 2
            else:
                n = tableau[0, 2:].tolist().index(np.amin(tableau[0, 2:])) + 2

            # тест на мінімум, тоді rth змінних виходять із базису
            minimum = 99999
            r = -1
            for i in range(1, len(tableau)):
                if (tableau[i, n] > 0):
                    val = tableau[i, 1] / tableau[i, n]
                    if val < minimum:
                        minimum = val
                        r = i

            pivot = tableau[r, n]
            # операція із рядками
            # ділимо ведучу стрічку на ведучий елемент
            tableau[r, 1:] = tableau[r, 1:] / pivot

            # ділимо інші стрічки
            for i in range(0, len(tableau)):
                if i != r:
                    mult = tableau[i, n] / tableau[r, n]
                    tableau[i, 1:] = tableau[i, 1:] - mult * tableau[r, 1:]
                    # нове значення базисної змінної
            tableau[r, 0] = n - 2
            iter += 1
        self.x = np.array([0] * len(c), dtype=float)
        # збергієамо коефіцієнти
        for key in range(1, (len(tableau))):
            if (tableau[key, 0] < len(c)):
                self.x[int(tableau[key, 0])] = tableau[key, 1]

        self.optimalValue = -1 * tableau[0, 1]

b = np.array([1, 1, 1, 1])
c = np.array([1, 1, 1, 1, 1])
model1 = LinearModel(optimized, b, c)

model1.optimize()
model1.printSoln()
