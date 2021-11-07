class Option():
    def __init__(self, order, count):
        self.order = order
        self.count = count
        pass

candidates = ["А","Б","С"]
list = [
    Option(["А","Б","С"], 24),
    Option(["А","С","Б"], 23),
    Option(["Б","А","С"], 26),
    Option(["Б","С","А"], 6),
    Option(["С","А","Б"], 12),
    Option(["С","Б","А"], 19)
]

# метод Борда
candidatesCount = len(candidates) - 1
candidatesCount
points = {x:sum([y.count * (candidatesCount - y.order.index(x)) for y in list]) for x in candidates}
points
bestCandidate = max(points, key = lambda item: points[item])
print(f'Найкращий кандидат - {bestCandidate}. Він набрав {points[bestCandidate]} голосів за методом Борда')



# метод Кондорсе
import itertools
def compare(pair, list):
    sum1, sum2 = 0, 0
    for x in list:
        if x.order.index(pair[0]) < x.order.index(pair[1]):
            sum1 += x.count
        else:
            sum2 += x.count
    print(f'{pair[0]} : {sum1} vs {pair[1]} : {sum2}')
    return [pair[0],pair[1]] if sum1 > sum2 else [pair[1],pair[0]]

combinations = [x for x in itertools.combinations(candidates,2)]
compared = [compare(pair, list) for pair in combinations]
compared
dominated = [x[0] for x in compared]
print(f'За методом Кондорсе домінує кандидат {max(set(dominated), key=dominated.count)}')
