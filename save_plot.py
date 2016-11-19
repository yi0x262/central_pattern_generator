import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import datetime

class logger(object):
    def __init__(self,lognames):
        """
        lognames: [name1,name2,...] name:str
        logdata : [[data1_0,data1_1,...],[data2_0,...],...]
        """
        self.logdata = [list() for _ in range(len(lognames))]
        self.lognames = lognames
    def append(self,data):
        """
        data    : [data1_t,data2_t,data3_t,...]
        """
        for i,datum in enumerate(data):
            self.logdata[i].append(datum)#[:])#get copy
    def output(self,logpath,t,title=None,each_axes_save=False,show=False):
        """
        logpath : abs dir path
        """
        os.makedirs(logpath,exist_ok=True)
        savedir = logpath+'/'+datetime.now().strftime('%Y%m%d_%H%M%S')#get nowtime(YearmonthDay_HourMinuteSecond)

        figure = plt.figure(figsize=(8,3*len(self.lognames)))
        for i,(datum,name) in enumerate(zip(self.logdata,self.lognames)):
            axes = figure.add_subplot(len(self.lognames),1,i+1)
            self.generate_each_graph(axes,t,datum,savedir,name,each_axes_save)

        #
        if not title is None:
            figure.suptitle(title,fontsize=12)

        figure.savefig(savedir+'.jpg')
        if show:
            figure.show()
    def generate_each_graph(self,axes,x,y,savedir,name,saveflag):
        """
        savepath: abs path
        data    : [data_0,data_1,...]
        """
        axes.plot(x,y)
        axes.set_title(name)

        if saveflag:
            #for saving
            os.makedirs(savedir,exist_ok=True)
            fig = plt.figure()
            ax  = fig.add_subplot(111)
            ax.plot(x,y)
            figure.savefig(savedir+'/'+name+'.jpg')


if __name__ == '__main__':
    import numpy as np
    x = np.hsplit(np.arange(100),4)
    log = logger(['one','two','three','four'])
    for on,tw,th,fo in zip(x[0],x[1],x[2],x[3]):
        log.append([on,tw,th,fo])
    log.output('/home/yihome/test',x[0],show=True)
