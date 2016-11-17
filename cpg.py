#!/usr/env/bin python3
import numpy as np
from scipy.integrate import odeint

#Sustained Oscillations Generated by Mutually Inhibiting Neurons with Adaptation,Matsuoka,1985
class cpg(object):
    def __init__(self,num,A,b=1,T=1):
        """
        A (const) : strengths of an inhibitory connection between neurons
        b (const) : time cources of adaptation
        T (const) : time cources of adaptation
        """
        self.A = A
        self.b = b
        self.T = T

        self.g = np.tanh

        self.x = np.array([0.1,-0.1,-0,-0,0,0])
        self.num = num

    def __call__(self,t,s):
        """s:input vector"""
        self.x   = odeint(self.func,self.x,t,args=(self.num,s,self.A,self.b,self.T,self.g))
        return self.x

    def func(self,vector,t,num,s,A,b,T,g):
        """
        x[0]: voltage
        t   :
        s   : input
        x[1]: output
        x'  : adaptation
        b,T : time cources of adaptation (scalar?)

        dx/dt   = -x - yA + s + bx'
        dx'/dt  = (-x' + y)/T
        y       = g(x)
        """
        x = list(vector.reshape(3,num))
        #x_dt = (-x[0]-np.dot(x[2],A)+s+b*x[1])
        #xd_dt = (-x[1]+x[2])/T
        #y_dt = g(x[0])
        #print('vec',vector)
        #print('dt',x_dt,xd_dt,y_dt)
        #ret = np.r_[x_dt,xd_dt,y_dt]
        #print('ret',ret)
        #print('time',t)
        #print('s',s)
        #return ret
        return np.r_[(-x[0]-np.dot(x[2],A)+s+b*x[1]),(-x[1]+x[2])/T,g(x[0])]

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    neuronum = 2
    times = 100
    A = np.array([[0,2.5],[2.5,0]])
    c = cpg(neuronum,A,b=0.1,T=0.1)

    s = np.array([0.5,0.5])
    t = np.linspace(0,2,10001)
    y = c(t,s)
    #y = [d[2*neuronum:] for d in y]

    plt.plot(t,y)
    plt.show()
