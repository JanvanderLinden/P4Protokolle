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

###########################################
#fitte an data
###########################################
f=tb

###########################################
#function definitions
###########################################
def cut(arr,up,to):
    i,j = 0, 0
    while f[i] < up:
        i += 1
    j=i
    while f[j] < to:
        j += 1
    return arr[i:j]

lin = lambda x,a,b: a*x+b

def getf(up,to,name,c):
    x=cut(time,up,to)
    y=cut(f,up,to)
    erg,pcov=sc.curve_fit(lin,x,y)
    perr = np.sqrt(np.diag(pcov))
    print 'erg',name, erg
    print 'err',name, perr
    plt.plot(time2,lin(time2,*erg),label=name+';  m*x+b', color=c)
    plt.plot((1000,2300),(up,up),color=c,linewidth=.5)
    plt.plot((1000,2300),(to,to),color=c,linewidth=0.5)
    plt.text(1200,up+0.1,'limit for '+name+': '+str(up),fontsize=siz)
    plt.text(1200,to+0.1,'limit for '+name+': '+str(to),fontsize=siz)
    return erg, perr
    
def gauss(val,a,ad,b,bd):
    s1, s2=(val*ad/a)**2, (val*bd/b)**2
    return np.sqrt(s1 + s2 )

siz=8

###########################################
#getting raw data in relevant ranges, index = 580
###########################################
time2 = time[580:]
tb2 = tb[580:]
tp2 = tp[580:]

###########################################
#getting  fits and plot them
###########################################
f1, f1e = getf(85,88,'fit 1','red')
f2, f2e = getf(90.5,f[-1],'fit 2','green')
plt.text(1880,90,'f1',fontsize=siz)
plt.text(1840,88.5,'f2',fontsize=siz)
###########################################
#get distance and plot it
###########################################
a, b = 1800, 1800
while lin(a,*f1) < 90.5:
    a += 1
while lin(b,*f2) < 90.5:
    b += 1
#time wenn fit 1 lim erreicht
t1 = a
#time wenn fit 2 lim erreicht
t2 = b
#time differenz die gesucht ist
d = t2 - t1 
print d
plt.plot((t1,t1),(84,92),color='black')
plt.plot((t2,t2),(84,92),color='black')
plt.text(t1+10,89,'t1',fontsize=siz)
plt.text(t2+10,89,'t2',fontsize=siz)

###########################################
#print results
###########################################
xpos = 2320
p = 90.5
p0 = 0.7
c = 0

plt.text(xpos,(p-p0*c),(r'$fit 1:f_1 = m_1 \cdot t + b_1$'),fontsize=siz)
c=c+1
print '1', f1[0], f1e[0]
plt.text(xpos,(p-p0*c),r'$m_1 = 0.0057 \pm  4\cdot 10^{-6}$',fontsize=siz)
c=c+1
print '2', f1[1], f1e[1]
plt.text(xpos,(p-p0*c),r'$b_1 = 79 \pm  0.005$',fontsize=siz)
c=c+1
plt.text(xpos,(p-p0*c),(r'$fit 2: f_2 = m_2 \cdot t + b_2$'),fontsize=siz)
c=c+1
print '3', f2[0], f2e[0]
plt.text(xpos,(p-p0*c),r'$m_2 = 0.0053 \pm  6\cdot 10^{-6}$',fontsize=siz)
c=c+1
print '4', f2[1], f2e[1]
plt.text(xpos,(p-p0*c),r'$b_2 = 79.2 \pm  0.014$',fontsize=siz)
c=c+1
plt.text(xpos,(p-p0*c),(r'$t1/2:\quad f_{1/2} \stackrel{!}{=} 90.5 $'),fontsize=siz)
c=c+1
print 't1', t1, 't2', t2,'d',d
#t1error = 1.66 t2error = 3.57
plt.text(xpos,(p-p0*c),(r'$t_2-t_1=(114 \pm 3.9)s$'),fontsize=siz)


###########################################
#plot general settings
###########################################
#plt.plot(time,tb,label="cup temperature")
plt.plot(time,tb,label='sample temperature')

plt.legend(loc=8,fontsize=siz)
plt.subplots_adjust(top=0.7,right=0.99)
plt.xlabel('Time in s', fontsize=siz)
plt.ylabel('Temperature in K', fontsize=siz)
plt.xlim(1080,2700)
plt.ylim(84.5,92)
#plt.grid()
plt.savefig("latent_j.pdf")
plt.show()