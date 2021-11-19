import pandas as pd
import numpy as np

df = pd.read_csv("Kruvui\\lab4\\lab4_data.csv", header=None)
df
vag = np.array(df[1][1:], dtype='f')
coef = {df[i][0] :np.array(df[i][1:], dtype='f') for i in range(2,6)}
coef
ratings = {x:np.array(vag * coef[x]).sum() for x in coef}
city = max(ratings, key=ratings.get)

print(f"Найкраще рішення: {ratings[city]}, це є {city}")
