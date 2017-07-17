import numpy as np
import itertools as it
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib
matplotlib.rcParams.update({"font.size": 14})

data = np.genfromtxt("SW_18", skip_header=2)
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
'''
plt.plot(t,signal)
plt.show()
plt.clf()
'''
rev_neg_t = t[:max_index]
neg_t = [-ti for ti in rev_neg_t]
pos_t = t[max_index:]
pos_sw = signal[max_index:]
neg_sw = signal[:max_index]

cutp = 4
cutn = 4
neg_t = neg_t[:-cutn]
rev_neg_t = rev_neg_t[:-cutn]
pos_t = pos_t[cutp:]
neg_sw = neg_sw[:-cutn]
pos_sw = pos_sw[cutp:]

log_nt = np.log10(neg_t)
log_pt = np.log10(pos_t)
log_nsw = np.log10(neg_sw)
log_psw = np.log10(pos_sw)


f = lambda t,A,a: np.log10(A/a)-a*t

#fit negatives
popt_n, pcov_n = curve_fit(f,log_nt,log_nsw)

#fit positives
popt_p, pcov_p = curve_fit(f,log_pt,log_psw)

fit_tp = np.linspace(0.001,0.12,1000)
fit_tn = np.linspace(-0.12,-0.001,1000)
fit_tn_rev = [-ti for ti in fit_tn]
fit_tpl = np.log10(fit_tp)
fit_tnl = np.log10(fit_tn_rev)


fit_n = f(fit_tnl,*popt_n)
fit_p = f(fit_tpl,*popt_p)
print(popt_n)
print(popt_p)
'''
plt.plot(log_nt,log_nsw, ".", label = "neg")
plt.plot(log_pt,log_psw, ".",label = "pos")
plt.plot(fit_tnl,fit_n)
plt.plot(fit_tpl,fit_p)
plt.legend()
plt.show()
plt.clf()
'''
# rescale
re_fit_n = 10**fit_n
re_fit_p = 10**fit_p

plt.rc("text", usetex = True)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel("$t = \\frac{T - T_N}{T_N}$", fontsize = 16)
plt.ylabel("reduced specific heat / $\\frac{\\textrm{J}}{\\textrm{K} \\cdot \\textrm{mol}}$", fontsize = 16)
plt.plot(t,signal, ".", color = "black", label = "data")
plt.plot(fit_tn, re_fit_n, lw = 1.5, color = "red", label = "fit for negative t")
plt.plot(fit_tp, re_fit_p, lw = 1.5, color = "blue", label = "fit for positive t")

ax.text(0.03,0.97,
	"fitted function:\n$%s$\nnegative times:\n$A^- = %.3f \\pm %.3f$\n$\\alpha = %.3f \\pm %.3f$\npositive times:\n$A^+ = %.3f \\pm %.3f$\n$\\alpha = %.3f \\pm %.3f$"%(
	"\\ln(c(t)) = \\ln\\left( \\frac{A^\\pm}{\\alpha}\\right) - \\alpha \\ln(t)",
	popt_n[0], np.sqrt(pcov_n[0][0]), popt_n[1], np.sqrt(pcov_n[1][1]),
	popt_p[0], np.sqrt(pcov_p[0][0]), popt_p[1], np.sqrt(pcov_p[1][1])),
	bbox = {"facecolor": "white"}, va = "top", ha = "left",
	fontsize = 14, transform = ax.transAxes)

plt.grid()
plt.legend()
plt.plot()
'''
plt.plot(t,signal)
plt.plot(t,sw)
plt.plot(pos_t,pos_sw, label = "pos")
plt.plot(neg_t,neg_sw, label = "neg")
plt.legend()
'''
plt.show()
