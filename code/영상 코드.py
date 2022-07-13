## %matplotlib auto

import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt

data=pd.read_excel(r"C:\Users\seohee\Downloads\29data.xlsx")
print(data)
count=0
x=[]
y=[]

def draw_graph(i):
    global count
    count +=1
    x.append(data['datetime'][count])
    y.append(data['power(kWh)'][count])

    plt.cla()
    plt.plot(x,y)
    
anima= animation.FuncAnimation(plt.gcf(),draw_graph,interval=1500)
plt.title("number : 29")
plt.legend(['y_train','y_pred'],
            loc='upper left')

plt.show()










