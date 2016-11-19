import matplotlib
import matplotlib.pyplot as plt
import os
from datetime import datetime

class plotter(object):#matplotlib.figure.Figure):
    def __init__(self):
        #super(self).__init__()
        pass
    def save_data(self,logpath,lognames,data,each_axes_save=False,show=False):
        """
        logpath : abs dir path
        lognames: [name1,name2,...] name:str
        data    : [[data1_0,data1_1,...],[data2_0,...],...]
        """
        os.makedirs(logpath,exist_ok=True)
        timestr = datetime.now().strftime('%Y%m%d_%H%M%S')#get nowtime(YearmonthDay_HourMinuteSecond)
        figure = plt.figure(figsize=(8,3*len(lognames)))
        for i,(datum,name) in enumerate(zip(data,lognames)):
            self.generate_each_graph(figure.add_subplot(len(lognames),1,i+1),datum,logpath+'/'+timestr+'/'+name+'.jpg',each_axes_save)
        if show:
            figure.show()
        figure.savefig(logpath+'/'+timestr+'.jpg')
    def generate_each_graph(self,axes,data,savepath,each_axes_save):
        """
        savepath: abs path
        data    : [data_0,data_1,...]
        """
        #axes.title(os.path.basename(savepath).split('.')[0])#????text is not calable?
        axes.plot(range(len(data)),data)
        if not each_axes_save:
            return 0
        #for saving
        os.makedirs(os.path.dirname(savepath))
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        ax.plot(range(len(data)),data)
        figure.savefig(savepath)

class logger(plotter):
    def __init__(self,lognames,logpath):
        super(plotter).__init__()
        self.logdata = [list() for _ in range(len(lognames))]
        self.lognames,self.logpath = lognames,logpath
    def append(self,data):
        """
        data    : [data1_t,data2_t,data3_t,...]
        """
        for i,datum in enumerate(data):
            self.logdata[i].append(datum)#[:])#get copy
    def output(self,each_axes_save=False,show=False):
        self.save_data(self.logpath,self.lognames,self.logdata,each_axes_save=each_axes_save,show=show)

if __name__ == '__main__':
    import numpy as np
    x = np.hsplit(np.arange(100),4)
    log = logger(['one','two','three','four'],'/home/yihome/test')
    for on,tw,th,fo in zip(x[0],x[1],x[2],x[3]):
        log.append([on,tw,th,fo])
    log.output(show=True)

    while 1:
        pass
