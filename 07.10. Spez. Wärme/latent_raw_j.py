import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sc


###########################################
#getting raw data
###########################################
data=np.genfromtxt("latent_18.txt",skip_header=1)
time=data[:,0]
tb = data[:,1]
tp = data[:,2]

siz=8

###########
#plot general settings
###########################################
plt.plot(time,tp,label="cup temperature")
plt.plot(time,tb,label='sample temperature')

plt.legend(loc=8,fontsize=siz)

plt.xlabel('Time in s', fontsize=siz)
plt.ylabel('Temperature in K', fontsize=siz)
#plt.xlim(1080,2700)
#plt.ylim(84.5,92)
plt.grid()
#plt.savefig("latent_raw_j.pdf")
#plt.show()
p=10.7
t=4
m=0.056
print p*t/m
