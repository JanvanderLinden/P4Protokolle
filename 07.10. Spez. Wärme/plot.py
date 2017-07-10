import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sc



data=np.genfromtxt("latent_18.txt",skip_header=1)

time=data[:,0]
tb = data[:,1]
tp = data[:,2]

def cut(arr):
    i = 0
    while tp[i] < up:
        i += 1
    j=i
    while tp[j] < to:
        j += 1
    return arr[i:j]

up=85
to=tp[-1]
time85 = cut(time)
tb85 = cut(tb)
tp85 = cut(tp)
####erster fit
up=85
to=88
time2=cut(time)
tb2=cut(tb)
plt.plot(time2,tb2)

func = lambda x,a,b: a*x+b


param=sc.curve_fit(func,time2,tb2)
print param


#plt.plot(time85,tb85)
plt.plot(time85,tp85)
plt.show()
