import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = np.genfromtxt("SW_test.txt", skip_header=2)
T = data[400:,0]
sw = data[400:,1]

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
plt.show()
plt.clf()
rev_neg_t = t[:max_index]
neg_t = [-ti for ti in rev_neg_t]
pos_t = t[max_index:]
pos_sw = signal[max_index:]
neg_sw = signal[:max_index]

cut = 3
neg_t = neg_t[:-cut]
rev_neg_t = rev_neg_t[:-cut]
pos_t = pos_t[cut:]
neg_sw = neg_sw[:-cut]
pos_sw = pos_sw[cut:]

log_nt = np.log10(neg_t)
log_pt = np.log10(pos_t)
log_nsw = np.log10(neg_sw)
log_psw = np.log10(pos_sw)


f = lambda t,A,a: np.log10(A/a)-a*t

#fit negatives
popt_n, pcov_n = curve_fit(f,log_nt,log_nsw)

#fit positives
popt_p, pcov_p = curve_fit(f,log_pt,log_psw)

fit_n = f(log_nt,*popt_n)
fit_p = f(log_pt,*popt_p)

plt.plot(log_nt,log_nsw, ".", label = "neg")
plt.plot(log_pt,log_psw, ".",label = "pos")
plt.plot(log_nt,fit_n)
plt.plot(log_pt,fit_p)
plt.legend()
plt.show()
plt.clf()

# rescale
re_fit_n = 10**fit_n
re_fit_p = 10**fit_p
plt.plot(t,signal)
plt.plot(rev_neg_t, neg_sw, "o", color = "black")
plt.plot(pos_t, pos_sw, "o", color = "black")
plt.plot(rev_neg_t, re_fit_n, lw = 1.5, color = "red")
plt.plot(pos_t, re_fit_p, lw = 1.5, color = "red")
plt.plot()
'''
plt.plot(t,signal)
plt.plot(t,sw)
plt.plot(pos_t,pos_sw, label = "pos")
plt.plot(neg_t,neg_sw, label = "neg")
plt.legend()
'''
plt.show()
