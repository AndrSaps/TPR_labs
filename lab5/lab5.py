import numpy as np

class Matrix():

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
        temp = self.values
        for i in range(len(self.values)):
            optimized_1 = [[np.all(x - y>=0)  for x in temp].count(True) == 1 for y in temp]
            temp = temp[optimized_1]
            optimized_2 = [[np.all(x - y >=0)  for x in temp.T].count(True) == 1 for y in temp.T]
            temp = temp.T[optimized_2].T
        return temp

values = np.genfromtxt("Kruvui\\lab5\\lab5_data.csv",delimiter=',')
values
matrix = Matrix(values)

matrix.find_point()

matrix.optimal_strategy()

optimized = matrix.optimize()
optimized


import pulp
x1 = pulp.LpVariable("x1", lowBound=0)
x2 = pulp.LpVariable("x2", lowBound=0)
x3 = pulp.LpVariable("x3", lowBound=0)

prob = pulp.LpProblem('Завдання', pulp.LpMaximize)
prob += x1 + x2 + x3
prob += 13*x1 + 10*x2 + 14*x3 <= 1
prob += 12*x1 + 14*x2 + 10*x3 <= 1
prob += 9*x1 + 11*x2 + 14*x3 <= 1
prob.solve()
[f'{v} = {v.varValue}' for v in prob.variables()]
print(f'Результат: {pulp.value(prob.objective)}')
