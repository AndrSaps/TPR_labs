import numpy as np

class Matrix():
    """docstring for Matrix."""

    def __init__(self, values = []):
        self.values = np.array(values)
        # T означає транспоновану матриця

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

matrix = Matrix([
    [9,13,10,7,14],
    [10,9,10,11,13],
    [9,12,14,7,10],
    [13,9,11,10,7],
    [13,9,11,10,14]
])

matrix.find_point()

optimal = matrix.optimal_strategy()
