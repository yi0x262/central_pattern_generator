#!/usr/env/bin python2
import numpy as np
from scipy.integrate import odeint

#Sustained Oscillations Generated by Mutually Inhibiting Neurons with Adaptation,Matsuoka,1985
#Enhancing Humanoid Learning Abilties; Scalable Learning through Task-Relevant Features (Matsubara,2007)

class cpg(object):
    def __init__(self,num,A,b=2.5,T=12,tau=1,x0=None):
        """
        A (const) : strengths of an inhibitory connection between neurons (i!=j:aij>0,i==j:aij=0)
        b (const) : time cources of adaptation (2.5)
        T (const) : time cources of adaptation (12)
        """
        self.num = num
        self.b = b
        self.T = T
        self.tau = tau

        self.A = np.array(A)
        if x0 is None:
            x0 = np.zeros(num*2)
        self.x = np.array(x0)

    def g(self,x):
        """g(x) = max(0,x)"""
        return np.maximum(0,x)

    def __call__(self,dt,s,devide=1000):
        """s:input vector (ndim = 1)"""
        t = np.linspace(0,dt,devide+1)
        #print('cpg_call',s,self.x)
        self.x = odeint(self.func,self.x,t,args=(s,))[-1]
        return self.output()#return y

    def output(self):
        """y = g(x)"""
        return self.g(self.x[:self.num])

    def func(self,vector,t,s):
        """
        x[0]: voltage
        x[1]: adaptation
        s   : input
        b,T : time cources of adaptation (scalar?)
        y   : output. y = g(x) = max(0,x)
        tau : time cources for frequence

        tau*dx0/dt   = -x0 - yA + s - bx1
        tau*dx1/dt  = (-x1 + y)/T
        """
        x0,x1 = np.hsplit(vector,2)#vector.ndim = 1
        y = self.output()
        #print('cpg x',x0,x1,y,s)
        #print(-x0-y.dot(self.A)+s-self.b*x1)
        return self.tau*np.r_[-x0-y.dot(self.A)+s-self.b*x1,(-x1+y)/self.T]


if __name__ == '__main__':
    from save_plot import logger

    neuronum = 4
    a = 2.5
    #A = a - a*np.eye(neuronum)
    A = a - a*np.tri(neuronum)
    A += A.T
    print(A)
    #x0 = [0.25,-0.32]
    #x0 = [0.6,0.4,0.2,0]
    x0 = [0.01 * i for i in range(neuronum)]
    #x0 = x0+[0.081 for _ in range(neuronum)]
    x0 = x0+[0 for _ in range(neuronum)]
    print(x0)

    c = cpg(neuronum,A,x0=x0,tau=2)

    s = np.ones(neuronum)*0.1
    t = list(np.linspace(0,200,10001))#about 340times/s (Ubuntu,i5-4200m @ 2.5GHz)
    lgr = logger(['voltage','adaptation','output'])
    for t1,t2 in zip(t[:-1],t[1:]):
        dt = t2-t1
        y = c(dt,s)
        lgr.append(np.hsplit(np.r_[c.x,y],3))

    lgr.output('/home/yihome/Pictures/log/cpg/',t[:-1],show=True,
        title='$A=a-a*tri$,a={},s={},b={},T={},$\\tau$={},g=max\nx0={}'.format(a,s,c.b,c.T,c.tau,x0))
