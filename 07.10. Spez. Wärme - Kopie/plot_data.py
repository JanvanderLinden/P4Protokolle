import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sci
import matplotlib
matplotlib.rcParams.update({"font.size": 20})
plt.rc("text", usetex = True)
data = np.genfromtxt("SW_18", skip_header=2)
plt.plot(data[:,0],data[:,1], lw = 1.5, color = "black")
plt.xlim([80,200])
plt.legend()


plt.xlabel("Temperature $T$ / $\\textrm{K}$", fontsize = 16)
plt.ylabel("specific heat $C$ / $\\frac{\\textrm{J}}{\\textrm{K} \\cdot \\textrm{mol}}$", fontsize = 16)
plt.grid()
plt.show()

