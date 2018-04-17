# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:58:51 2018

@author: jlm7
"""

import numpy as np
from lmfit.models import StepModel, LinearModel
import matplotlib.pyplot as plt
from scipy import asarray as exp
from lmfit import Model
from scipy.optimize import curve_fit
from termcolor import colored

class determine_tc(object):
    """
    
    """
    def __init__(self, xdata, ydata, channel):
        y_data_1 = [y for y, x in sorted(zip(xdata, ydata))]
        x_data_1 = [x for y, x in sorted(zip(xdata, ydata))]

        self.ydata = x_data_1
        self.xdata = y_data_1
        self.channel = channel
        self.create_fit_line()
        
    def create_fit_line(self):
        step_mod = StepModel(form='erf', prefix='step_')
        line_mod = LinearModel(prefix='line_')
        
        pars =  line_mod.make_params(intercept=0, slope=0)
        pars += step_mod.guess(self.ydata, x=self.xdata, center=2)
        
        mod = step_mod + line_mod
        self.data_fit_line = mod.fit(self.ydata, pars, x=self.xdata)
        
    def plot_fit(self):
        plt.plot(self.xdata, self.ydata, '*', label="Data " + str(self.channel))
        plt.plot(self.xdata, self.data_fit_line.best_fit, '-', label="Fit " + str(self.channel))
        plt.xlabel("Temp")
        plt.ylabel("Resistance")
        plt.legend()
        plt.title("Critical Temperature")
        
    def calc_all(self):
        self.plot_fit()
        self.tc_onset_calculate()
        self.tc_90_10_calcuate()
        self.tc_gaussian_calculate()
        self.tc_x_intercept_calculate()
        self.fifty_percent_calculate()
        
    def tc_onset_calculate(self):
        self.d = np.gradient(self.data_fit_line.best_fit)
        self.dd = np.gradient(self.d)
        self.dd[np.abs(self.dd) < 0.001] = 0
#        plt.plot(self.xdata, self.dd)
#        self.begin_ind = next((i for i, x in enumerate(self.dd) if x), None)
#        self.end_ind = len(self.dd) - next((i for i, x in enumerate(reversed(self.dd)) if x), None)
        valmin, self.end_ind = min((valmin, idxmin) for (idxmin, valmin) in enumerate(self.dd))
        valmax, self.begin_ind = max((valmax, idxmax) for (idxmax, valmax) in enumerate(self.dd))
        self.onset = self.xdata[self.begin_ind]
        self.endpoint = self.xdata[self.end_ind]
        print("\n\nOnset/Endpoint Method:")
        print(np.round(self.onset,3)," ≤ Tc ≤ ", np.round(self.endpoint,3))
        print("ΔTc = ", np.round(self.endpoint - self.onset,3))
        
    def tc_90_10_calcuate(self):
        Tc_rise = self.ydata[self.end_ind] - self.ydata[self.begin_ind]

        res_10 = Tc_rise*0.1
        res_90 = Tc_rise*0.9
        for self.ind_10, x in enumerate(self.ydata):
            if x > res_10:
                break
        for self.ind_90, x in enumerate(self.ydata):
            if x > res_90:
                break
        
        self.tc_10 = self.xdata[self.ind_10]
        self.tc_90 = self.xdata[self.ind_90]
        print("\n\n90/10 Method:")
        print(np.round(self.tc_10,3)," ≤ Tc ≤ ", np.round(self.tc_90,3))
        print("ΔTc = ", np.round(self.tc_90 - self.tc_10,3))

    def tc_gaussian_calculate(self):
        def func(x, a, x0, sigma):
            return a*np.exp(-(x-x0)**2/(2*sigma**2))
        
        try:
            popt, pcov = curve_fit(func, self.xdata, self.d)
            ym = func(self.xdata, popt[0], popt[1], popt[2])
#            plt.plot(self.xdata, ym, "g")
        
    
            
            valmin, idxmin = min((valmin, idxmin) for (idxmin, valmin) in enumerate(np.gradient(ym)))
            valmax, idxmax = max((valmax, idxmax) for (idxmax, valmax) in enumerate(np.gradient(ym)))
            
            self.tc_gauss_low = self.xdata[idxmax]
            self.tc_gauss_high = self.xdata[idxmin]
            print("\n\nGaussian Inflection Point Method:")
            print(np.round(self.tc_gauss_low,3)," ≤ Tc ≤ ", np.round(self.tc_gauss_high,3))
            print("ΔTc = ", np.round(self.tc_gauss_high - self.tc_gauss_low,3))
        except:
            print("\n\nGaussian Inflection Point Method:")
            print(colored("ERROR in gaussian determiniation of chanel ", color="red"),colored(self.channel, color="red"))
    def tc_x_intercept_calculate(self):
        # Use Onset/Endpoint to get slope
#        slope1 = (res[end_ind]-res[begin_ind]) / (temp[end_ind]-temp[begin_ind])
#        line_data1 = slope1*(temp-temp[begin_ind])+res[begin_ind] # y-y1 = m(x-x1)
#        
        # Use 90/10 to get slope
        try:
            slope2 = (self.ydata[self.ind_90]-self.ydata[self.ind_10]) / (self.xdata[self.ind_90]-self.xdata[self.ind_10])
            self.tc_x_int = (-self.ydata[self.ind_10]/slope2)+self.xdata[self.ind_10]
            print("\n\nX-Intercept Method:")
            print("Tc = ", np.round(self.tc_x_int,3))

#        self.line_data2 = slope2*(self.xdata-self.xdata[self.ind_10])+self.ydata[self.ind_10] # y-y1 = m(x-x1)
        except:
            print("\n\nX-Intercept Method:")
           
            print(colored("ERROR in x intercept of channel ", color="red"),colored(self.channel, color="red"))
            
        # Use gaussian to get slope
#        slope3 = (res[idxmin]-res[idxmax]) / (temp[idxmin]-temp[idxmax])
#        line_data3 = slope2*(temp-temp[idxmax])+res[idxmax] # y-y1 = m(x-x1)
    
    def fifty_percent_calculate(self):
        top = self.ydata[self.begin_ind]
        bottom = self.ydata[self.end_ind]
        mid_value = (top+bottom)/2
        index = (np.abs(np.array(self.data_fit_line.best_fit) - mid_value)).argmin()
        self.fifty_percent_val = self.xdata[index]
        print("\n\n50% Method:")
        print("Tc = ", np.round(self.fifty_percent_val,3))
        



#%% Create Fake Data
res = []
temp = np.linspace(0,20,200)
for x in range(80):
    res.append((np.random.rand()-1))
res.append(1.1)
res.append(4.8)
res.append(19.1)
res.append(36.8)
res.append(42.1)
res.append(44.3)
res.append(46.7)
res.append(48.9)
res.append(49.1)
res.append(50.0)
for x in range(110):
    res.append(50 + x/14 +5*(np.random.rand()-1))


if (__name__ == "__main__"):
    test = determine_tc(temp, res,1)
    test.calc_all()




#    
##%% Create Fit for that data
#step_mod = StepModel(form='erf', prefix='step_')
#line_mod = LinearModel(prefix='line_')
#
#pars =  line_mod.make_params(intercept=0, slope=0)
#pars += step_mod.guess(res, x=temp, center=2)
#
#mod = step_mod + line_mod
#out = mod.fit(res, pars, x=temp)
#
##%% Plot
#plt.plot(temp, res)
#plt.plot(temp, out.best_fit, 'r-')
#plt.xlabel("Temp")
#plt.ylabel("Resistance")
#plt.title("Critical Temperature")
#
#
#
##%% Caluclate Tc Onset-Endpoint
#
#d = np.gradient(out.best_fit)
#dd = np.gradient(d)
#dd[np.abs(dd) < 0.001] = 0
#begin_ind = next((i for i, x in enumerate(dd) if x), None)
#end_ind = len(dd) - next((i for i, x in enumerate(reversed(dd)) if x), None)
#
#onset = temp[begin_ind]
#endpoint = temp[end_ind]
#
##%% Calculate Tc 90-10
#Tc_rise = res[end_ind] - res[begin_ind]
#
#res_10 = Tc_rise*0.1
#res_90 = Tc_rise*0.9
#for ind_10, x in enumerate(res):
#    if x > res_10:
#        break
#for ind_90, x in enumerate(res):
#    if x > res_90:
#        break
#
#tc_10 = temp[ind_10]
#tc_90 = temp[ind_90]
#
##%% Calculate Tc Gaussian Fit 
#
#
#x = temp
#y = d
#
#
#def gaussian(x, amp, cen, wid):
#    """1-d gaussian: gaussian(x, amp, cen, wid)"""
#    return (amp / (np.sqrt(2*np.pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2))
#
#
#gmodel = Model(gaussian)
#result = gmodel.fit(y, x=x, amp=5, cen=5, wid=1)
#
##plt.plot(x, y, 'bo')
##plt.plot(x, result.best_fit, 'r-')
##plt.show()
#gauss_fit = result.best_fit
#
#valmin, idxmin = min((valmin, idxmin) for (idxmin, valmin) in enumerate(dd))
#valmax, idxmax = max((valmax, idxmax) for (idxmax, valmax) in enumerate(dd))
#
#tc_gauss_low = temp[idxmax]
#tc_gauss_high = temp[idxmin]
#
##%% Calculate X-intercept gaussian fit
#
## Use Onset/Endpoint to get slope
#slope1 = (res[end_ind]-res[begin_ind]) / (temp[end_ind]-temp[begin_ind])
#line_data1 = slope1*(temp-temp[begin_ind])+res[begin_ind] # y-y1 = m(x-x1)
#
## Use 90/10 to get slope
#slope2 = (res[ind_90]-res[ind_10]) / (temp[ind_90]-temp[ind_10])
#line_data2 = slope2*(temp-temp[ind_10])+res[ind_10] # y-y1 = m(x-x1)
#
## Use gaussian to get slope
#slope3 = (res[idxmin]-res[idxmax]) / (temp[idxmin]-temp[idxmax])
#line_data3 = slope2*(temp-temp[idxmax])+res[idxmax] # y-y1 = m(x-x1)
#
##plt.plot(temp,line_data1,'g')
##plt.plot(temp,line_data2,'o')
##plt.plot(temp,line_data3,'k')
#
#tc_x_int = (-res[ind_10]/slope2)+temp[ind_10]
##%% Display
#print("Tc Values:\n")
#print("90/10 Method:")
#print(np.round(tc_10,3)," ≤ Tc ≤ ", np.round(tc_90,3))
#print("\n\nOnset/Endpoint Method:")
#print(np.round(onset,3)," ≤ Tc ≤ ", np.round(endpoint,3))
#print("\n\nGaussian Inflection Point Method:")
#print(np.round(tc_gauss_low,3)," ≤ Tc ≤ ", np.round(tc_gauss_high,3))
#print("\n\nX-Intercept Method:")
#print("Tc = ", np.round(tc_x_int,3))
#plt.show()
#



























#
#import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#import numpy as np
#
#def log_func(x, a, b, c):
#    return (c - a * np.exp(-b * x))
#
#def exp_func(x, a, b, c):
#    return a * np.exp(-b * x) + c
#
#def lin_func(x, a, b):
#    return a * x + b
#
#def quad_func(x, a, b, c):
#    return a * np.power(x,2) + b * x + c
#
##%%
#
#xdata = np.linspace(0, 4, 500)
#y = log_func(xdata, 2.5, 1.3, 0.5)
#np.random.seed(19296)
#y_noise = 0.2 * np.random.normal(size=xdata.size)
#ydata = y + y_noise
#plt.plot(xdata, ydata, 'b-', label='data')
#
#popt, pcov = curve_fit(log_func, xdata, ydata)
#plt.plot(xdata, log_func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
##%%
#xdata = np.linspace(0, 4, 500)
#y = exp_func(xdata, 2.5, 1.3, 0.5)
#np.random.seed(19296)
#y_noise = 0.2 * np.random.normal(size=xdata.size)
#ydata = y + y_noise
#plt.plot(xdata, ydata, 'b-', label='data')
#
#popt, pcov = curve_fit(log_func, xdata, ydata)
#plt.plot(xdata, log_func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
##%%
#xdata = np.linspace(0, 4, 500)
#y = quad_func(xdata, 2.5, 1.3, 0.5)
#np.random.seed(19296)
#y_noise = 0.2 * np.random.normal(size=xdata.size)
#ydata = y + y_noise
#plt.plot(xdata, ydata, 'b-', label='data')
#
#popt, pcov = curve_fit(quad_func, xdata, ydata)
#plt.plot(xdata, quad_func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
##%%
#
#
#
##popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
##plt.plot(xdata, func(xdata, *popt), 'g--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
# 
#plt.xlabel('x')
#plt.ylabel('y')
#plt.legend()
#plt.show()
#
#
























#
#class fit_that_curve(object):
#    """
#    Use this to fit that curve
#    """
#    def __init__(self, xdata, ydata):
#        self.xdata = xdata
#        self.ydata = ydata
#        
#    def create_fit(self):
#        print(self.xdata, self.ydata)
#        
#    def make_graph(self:):
#        print(self.xdata, self.ydata)