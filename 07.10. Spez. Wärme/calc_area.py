import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sci

data = np.genfromtxt("SW_test.txt", skip_header=2)
T = data[:100,0]
sw = data[:100,1]

def cut_area(arr, min, max, arg):
	i = 0
	while T[i] < min:
		i+= 1
	j = i
	while T[j] < max:
		j+= 1
	if arg == "out":
		arr = [arr[index] for index in range(len(arr)) if index < i or index > j]
	elif arg == "in":
		arr = arr[i:j]
	return arr

bkgT = cut_area(T, 85, 95, "out")
bkgsw = cut_area(sw, 85, 95,"out" )

f = lambda x,a,b: a*x+b

popt, pcov = sci.curve_fit(f,bkgT,bkgsw)
bkgfit = f(T,*popt)

# plot 1: background fit
plt.plot(T,sw,".")
plt.plot(bkgT,bkgsw,".")
plt.plot(T,bkgfit, "-")
plt.show()


a_err = np.sqrt(pcov[0][0])
b_err = np.sqrt(pcov[1][1])
print(popt[0],a_err)
print(popt[1],b_err)

df = lambda x,a,b,da,db: np.sqrt( (x*da)**2 + db**2)

signal = sw - bkgfit
sig_err = [df(xx,popt[0],popt[1],a_err,b_err) for xx in sw]

plt.clf()
sigT = cut_area(T, 85,95,"in")
sigsw = cut_area(signal,85,95,"in")
sigsw_err = cut_area(sig_err,85,95,"in")

area = 0
sq_err = 0
for i in range(len(sigT)):
	try:
		area += sigsw[i]*(sigT[i+1]-sigT[i-1])/2.
		sq_err += (sigsw_err[i]*(sigT[i+1]-sigT[i-1])/2.)**2	
	except:
		continue
# plot2: signal region
plt.errorbar(sigT, sigsw,yerr = sigsw_err, fmt = "o")
plt.title("{:.3f}, {:.3f}".format(area, np.sqrt(sq_err)))
plt.show()




