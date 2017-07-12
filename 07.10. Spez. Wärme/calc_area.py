import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sci
import matplotlib
matplotlib.rcParams.update({"font.size": 14})
plt.rc("text", usetex = True)
data = np.genfromtxt("SW_18", skip_header=2)
T = data[:100,0]
sw = data[:100,1]
#plt.plot(data[:,0],data[:,1])
#plt.show()
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
fig = plt.figure()
ax = fig.add_subplot(111)

# plot 1: background fit
plt.plot(T,sw,".", color = "blue", label = "signal peak")
plt.plot(bkgT,bkgsw,".", color = "black", label = "background")
plt.plot(T,bkgfit, "-", color = "red", lw = 2, label = "background fit")
plt.legend()
plt.xlim([80,100])
plt.ylim([30,50])


a_err = np.sqrt(pcov[0][0])
b_err = np.sqrt(pcov[1][1])
print(popt[0],a_err)
print(popt[1],b_err)
df = lambda x,a,b,da,db: np.sqrt( (x*da)**2 + db**2)

signal = sw - bkgfit
sig_err = [df(xx,popt[0],popt[1],a_err,b_err) for xx in sw]

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

ax.text(0.03,0.97,
    "fitted background function:\n$%s$\n$m = %.3f \\pm %.3f$\n$b = %.3f \\pm %.3f$\ncalculated signal area:\n$A = %.3f \\pm %.3f$"%(
    "c(t) = m\\cdot T + b",
	popt[0], a_err,
	popt[1], b_err,
	area, np.sqrt(sq_err)),
	bbox = {"facecolor": "white"}, va = "top", ha = "left",
	fontsize = 14, transform = ax.transAxes)
plt.xlabel("Temperature $T$ / $\\textrm{K}$", fontsize = 16)
plt.ylabel("specific heat $C$ / $\\frac{\\textrm{J}}{\\textrm{K} \\cdot \\textrm{mol}}$", fontsize = 16)
plt.grid()
plt.show()
# plot2: signal region
'''
plt.errorbar(sigT, sigsw,yerr = sigsw_err, fmt = "o")
plt.title("{:.3f}, {:.3f}".format(area, np.sqrt(sq_err)))
plt.show()



'''
