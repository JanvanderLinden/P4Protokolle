import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sc


###########################################
#getting raw data
###########################################
data=np.genfromtxt("SW_18.txt",skip_header=1)
t=data[:,0]
ch = data[:,1]
tn=179.92

###########################################
#fitte an data
###########################################

###########################################
#function definitions
###########################################

def cut(arr,up,to):
    i,j = 0, 0
    while t[i] < up:
        i += 1
    j=i
    while t[j] < to:
        j += 1
    return arr[i:j]
def cut2(arr):
    i= 0
    while t2[i] < 0:
        i += 1    
    return arr[0:i], arr[i+1:-1]
def lin(x,a,b):
    return a*x+b
    
def exp(x,A,a):
    #alhpa=(0.1356+0.1818)/2
    return A*np.power(np.absolute(x),-a)/a

def getfp(x,y,name,c):
    erg,pcov=sc.curve_fit(exp,x,y)
    perr = np.sqrt(np.diag(pcov))
    print 'erg',name, erg
    print 'err',name, perr
    plt.plot(x,exp(x,*erg),label=r'$\frac{|t|^{-\alpha^+}}{\alpha^+}\cdot A^+$', color=c)
    return erg, perr
def getfm(x,y,name,c):
    erg,pcov=sc.curve_fit(exp,x,y)
    perr = np.sqrt(np.diag(pcov))
    print 'erg',name, erg
    print 'err',name, perr
    plt.plot(x,exp(x,*erg),label=r'$\frac{|t|^{-\alpha^-}}{\alpha^-}\cdot A^-$', color=c)
    return erg, perr

siz=12
E,B=25,16
lim1=tn*0.8
lim2=t[-1]

t2 = (cut(t,lim1,lim2)-tn)/tn#beschnitten
ch2 = cut(ch,lim1,lim2)#beschnitten 
ch3 = ch2 - lin(t2,E,B)#reduziert und beschnitten
max=0

cs1,cs2 = cut2(ch3)
ts1,ts2 = cut2(t2)

getfm(ts1,cs1,'minus','blue')
getfp(ts2,cs2,'plus','green')

plt.plot(ts1,cs1,color='black',label='raw data')
plt.plot(ts2,cs2,color='black')

###########################################
#print results
###########################################
xpos = -0.2
p = 74
p0 = 6
c = 0

plt.text(xpos,(p-p0*c),r'$\alpha^- = 0.136 \pm  0.002$',fontsize=siz)
c=c+1
plt.text(xpos,(p-p0*c),r'$\alpha^+ = 0.182 \pm  0.007$',fontsize=siz)
c=c+1
plt.text(xpos,(p-p0*c),(r'$A^- = (4.04 \pm 0.04)\,\rm{\frac{J}{mol\cdot K}}$'),fontsize=siz)
c=c+1
plt.text(xpos,(p-p0*c),r'$A^+ = (2.54 \pm 0.04)\,\rm{\frac{J}{mol\cdot K}}$',fontsize=siz)
c=c+1

###########################################
#plot general settings
###########################################
mol=1
E=25*mol
B=16*mol
#plt.plot(t2,lin(t2,E,B),label="untergrund")
#plt.plot(t2,ch3,label='sample temperature')

plt.legend(loc=0,fontsize=siz)
#plt.subplots_adjust(top=0.7,right=0.99)
plt.ylabel('specific heat'+r'$\,\frac{J}{K\cdot mol}$', fontsize=siz)
plt.xlabel(r'$t=\frac{T-T_N}{T_N}$', fontsize=siz)
plt.xlim(-.22,.13)
plt.ylim(20,80)
plt.grid()
plt.savefig("specheat_j.pdf")
plt.show()