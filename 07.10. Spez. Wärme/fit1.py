import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sci

data = np.genfromtxt("SW_test.txt", skip_header=2)
T = data[300:,0]
sw = data[300:,1]

max_index = 0
for i in range(len(sw)):
	if sw[i] > sw[max_index]:
		max_index = i

# Neel Temp:
TN = T[max_index]
print("Neel Temp: {:.3f}, Arrayindex: {:.3f}".format(TN, max_index))

# temperatur rescaling
t = [ (Ti - TN)/TN for Ti in T]

bkg = [ 25.*ti + 16. for ti in t]

signal = sw-bkg

plt.plot(t,signal)
plt.plot(t,sw)
plt.show()
