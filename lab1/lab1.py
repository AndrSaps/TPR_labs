# А)
import numpy as np
import pandas as pd
# задаємо матрицю списками списків
matrix=np.genfromtxt("Kruvui\\lab1\\lab1_matrix.csv",delimiter=',')

vald = matrix.min(axis=1)
vald
print("Критерій Вальда. Обираємо " + str(np.where(vald==vald.max())[0]+1)+" рядок, бо максимальне мінімальние = "+str(vald.max()))
#мінімальні елементи для усіх рядків
laplas=matrix.mean(axis=1)
laplas
print("Критерій Лапласа. Обираємо "+str(np.where(laplas == laplas.max())[0]+1)+" рядок, бо середнє арифметичне= "+str(laplas.max()))
#обраховуємо критерії Гурвіца та виводимо їх
#коефіцієнт для критерію Гурвіца
x=0.5
gurv=np.array([x*min(i)+(1-x)*max(i) for i in matrix])
gurv
print("Критерій Гурвіца. Обираємо "+str(np.where(gurv==gurv.max())[0]+1)+" рядок, бо за формулою отримуємо найбільшу відповідь = "+str(gurv.max()))
# Б)
p = np.array([0.55,0.3,0.15])
result = matrix * p
result
result_sum = result.sum(axis=1)
print("Критерій Баєса-Лапласа. Обираємо " + str(np.where(result_sum == result_sum.max())[0]+1)+" рядок, бо за формулою отримуємо найбільшу відповідь = " + str(result_sum.max()))

df=pd.DataFrame(columns=["Умова 1","Умова 2","Умова 3","Вальда","Лапласа","Гурвіца","Байеса-Лапласса"])
df.loc[1]=[*matrix[0], vald[0], laplas[0], gurv[0], result_sum[0]]
df.loc[2]=[*matrix[1], vald[1], laplas[1], gurv[1], result_sum[1]]
df.loc[3]=[*matrix[2], vald[2], laplas[2], gurv[2], result_sum[2]]
df.style.apply(lambda col: ["background: #ff33aa" if row == col.max() and not col.name.startswith("Умова") else "" for row in col], axis = 0)
