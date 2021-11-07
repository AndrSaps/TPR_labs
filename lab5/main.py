import numpy as np

f = open("data")
print('Отримана матриця:')
X = np.loadtxt(f)
print(X)
max_per_col = X.max(axis=0)
min_per_row = X.min(axis=1)
print('Мінімальні значення по рядках:', min_per_row)
print('Максимальні значення по стовпцях:', max_per_col)
print('Максимальне значення по рядках', max(min_per_row))
print('Мінімальне значення по стовпцях', min(max_per_col))
if(max(min_per_row)!=min(max_per_col)):
    print('Оскільки максимальні значення по рядках та стовпцях не рівні, '
          '\nзначить у нас відсутня сідлова точка, а ціна знаходиться у межах:')
    if(max(min_per_row)>min( max_per_col)):
        print(min(max_per_col),'<=',max(min_per_row))
    else:
        print(max(min_per_row), '<=', min(max_per_col))
else:
    print('У нас присутня сідлова точка, значення ціни становить',max(min_per_row))




fin = open('data','r')
matrix=[]
for line in fin.readlines():
    matrix.append( [ int (x) for x in line.split(' ') ] )

toremove = set()
toremove_new = set()
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if i == j:
            continue
        if all(map(lambda x: x[0] <= x[1], zip(matrix[i], matrix[j]))):
            print("Рядок", j+1, "домінує над рядком ",i+1)
            toremove.add(i)
            break
matrix = [matrix[i] for i in range(len(matrix)) if i not in toremove]
print("\nТепер матриця має вигляд: ")
for row in matrix:
    print(", ".join(map(str, row)))
print("\nТепер видаляємо стовпці.")
numpy_array = np.array(matrix)
transpose = numpy_array.T
transpose_list = transpose.tolist()


for i in range(len(transpose_list)):
    for j in range(len(transpose_list)):
        if i == j:
            continue
        if all(map(lambda x: x[0] >= x[1], zip(transpose_list[i], transpose_list[j]))):
            print("Стовпець", j + 1, "домінує над стовпцем ", i + 1)
            toremove_new.add(i)
            break
transpose_list = [transpose_list[i] for i in range(len(transpose_list)) if i not in toremove_new]
print("\nТепер матриця має вигляд: ")
numpy_array = np.array(transpose_list)
transpose = numpy_array.T
transpose_list_new = transpose.tolist()
for row in transpose_list_new:
    print(", ".join(map(str, row)))


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

    def setObj(self, minmax):
        if (minmax == "MIN" or minmax == "MAX"):
            self.minmax = minmax
        else:
            print("Шось не ясно, давай по нормальному або мін, або макс.")
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


model1 = LinearModel()

A = np.array(transpose_list_new)
b = np.array([1, 1, 1])
c = np.array([1, 1])

model1.addA(A)
model1.addB(b)
model1.addC(c)
model1.optimize()
model1.printSoln()

