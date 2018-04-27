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
    def __init__(self, xdata, ydata, channel, txt_file, graph_file, tc_guess=6):
        y_data_1 = [y for y, x in sorted(zip(xdata, ydata))]
        x_data_1 = [x for y, x in sorted(zip(xdata, ydata))]
        if(x_data_1 and y_data_1):
            self.tc_guess = tc_guess
            self.ydata = x_data_1
            self.xdata = y_data_1
            self.channel = channel
            self.create_fit_line()
            self.valid = True
            self.txt_file = txt_file
            self.graph_file = graph_file
        else:
            self.valid = False
            
        
    def create_fit_line(self):
        step_mod = StepModel(form='erf', prefix='step_')
        line_mod = LinearModel(prefix='line_')
        
        pars =  line_mod.make_params(intercept=0, slope=0)
        pars += step_mod.guess(self.ydata, x=self.xdata, center=self.tc_guess)
        xmin = np.min(self.xdata)
        xmax = np.max(self.xdata)
        self.x_fit_range = np.linspace(xmin, xmax, 1000)
        
        self.y_data_interp = np.interp(self.x_fit_range,self.xdata,self.ydata)
        pars2 =  line_mod.make_params(intercept=0, slope=0)
        pars2 += step_mod.guess(self.y_data_interp, x=self.x_fit_range, center=6)
        
        mod = step_mod + line_mod
#        self.data_fit_line = mod.fit(self.ydata, pars, x=self.xdata)
#        self.data_fit_line2 = np.interp(self.x_fit_range, self.xdata, self.data_fit_line.best_fit)
        
        
        self.data_fit_line = mod.fit(self.y_data_interp, pars2, x=self.x_fit_range)

        
    def plot_fit(self):
        plt.plot(self.xdata, self.ydata, '*', label="Data " + str(self.channel))
        plt.plot(self.x_fit_range, self.data_fit_line.best_fit, '-', label="Fit " + str(self.channel))

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
        self.write_file()
        plt.savefig(self.graph_file)
        
    def tc_onset_calculate(self):
#        self.d = np.gradient(self.data_fit_line.best_fit)
        self.d = np.gradient(self.data_fit_line.best_fit)
        self.dd = np.gradient(self.d)
        self.dd[np.abs(self.dd) < 0.001] = 0
#        plt.plot(self.xdata, self.dd)
#        self.begin_ind = next((i for i, x in enumerate(self.dd) if x), None)
#        self.end_ind = len(self.dd) - next((i for i, x in enumerate(reversed(self.dd)) if x), None)
        valmin, self.end_ind = min((valmin, idxmin) for (idxmin, valmin) in enumerate(self.dd))
        valmax, self.begin_ind = max((valmax, idxmax) for (idxmax, valmax) in enumerate(self.dd))
        self.onset = self.x_fit_range[self.begin_ind]
        self.endpoint = self.x_fit_range[self.end_ind]
        print("\n\nOnset/Endpoint Method:")
        print(np.round(self.onset,3)," ≤ Tc ≤ ", np.round(self.endpoint,3))
        print("ΔTc = ", np.round(self.endpoint - self.onset,3))

        
    def tc_90_10_calcuate(self):
        Tc_rise = self.data_fit_line.best_fit[self.end_ind] - self.data_fit_line.best_fit[self.begin_ind]

        res_10 = Tc_rise*0.1
        res_90 = Tc_rise*0.9
        for self.ind_10, x in enumerate(self.data_fit_line.best_fit):
            if x > res_10:
                break
        for self.ind_90, x in enumerate(self.data_fit_line.best_fit):
            if x > res_90:
                break
        
        self.tc_10 = self.x_fit_range[self.ind_10]
        self.tc_90 = self.x_fit_range[self.ind_90]
        print("\n\n90/10 Method:")
        print(np.round(self.tc_10,3)," ≤ Tc ≤ ", np.round(self.tc_90,3))
        print("ΔTc = ", np.round(self.tc_90 - self.tc_10,3))

    def tc_gaussian_calculate(self):
        def func(x, a, x0, sigma):
            return a*np.exp(-(x-x0)**2/(2*sigma**2))
        
        try:
            popt, pcov = curve_fit(func, self.x_fit_range, self.d)
            ym = func(self.x_fit_range, popt[0], popt[1], popt[2])
#            plt.plot(self.xdata, ym, "g")
        
    
            
            valmin, idxmin = min((valmin, idxmin) for (idxmin, valmin) in enumerate(np.gradient(ym)))
            valmax, idxmax = max((valmax, idxmax) for (idxmax, valmax) in enumerate(np.gradient(ym)))
            
            self.tc_gauss_low = self.x_fit_range[idxmax]
            self.tc_gauss_high = self.x_fit_range[idxmin]
            print("\n\nGaussian Inflection Point Method:")
            print(np.round(self.tc_gauss_low,3)," ≤ Tc ≤ ", np.round(self.tc_gauss_high,3))
            print("ΔTc = ", np.round(self.tc_gauss_high - self.tc_gauss_low,3))
            self.gfail = False
        except:
            self.gfail = True
            print("\n\nGaussian Inflection Point Method:")
            print(colored("ERROR in gaussian determiniation of chanel ", color="red"),colored(self.channel, color="red"))
    def tc_x_intercept_calculate(self):
        # Use Onset/Endpoint to get slope
#        slope1 = (res[end_ind]-res[begin_ind]) / (temp[end_ind]-temp[begin_ind])
#        line_data1 = slope1*(temp-temp[begin_ind])+res[begin_ind] # y-y1 = m(x-x1)
#        
        # Use 90/10 to get slope
        try:
            slope2 = (self.data_fit_line.best_fit[self.ind_90]-self.data_fit_line.best_fit[self.ind_10]) / (self.x_fit_range[self.ind_90]-self.x_fit_range[self.ind_10])
            self.tc_x_int = (-self.data_fit_line.best_fit[self.ind_10]/slope2)+self.x_fit_range[self.ind_10]
            print("\n\nX-Intercept Method:")
            print("Tc = ", np.round(self.tc_x_int,3))
            self.xfail = False

#        self.line_data2 = slope2*(self.xdata-self.xdata[self.ind_10])+self.ydata[self.ind_10] # y-y1 = m(x-x1)
        except:
            self.xfail = True
            print("\n\nX-Intercept Method:")
           
            print(colored("ERROR in x intercept of channel ", color="red"),colored(self.channel, color="red"))
            
        # Use gaussian to get slope
#        slope3 = (res[idxmin]-res[idxmax]) / (temp[idxmin]-temp[idxmax])
#        line_data3 = slope2*(temp-temp[idxmax])+res[idxmax] # y-y1 = m(x-x1)
    
    def fifty_percent_calculate(self):
        top = self.data_fit_line.best_fit[self.begin_ind]
        bottom = self.data_fit_line.best_fit[self.end_ind]
        mid_value = (top+bottom)/2
        index = (np.abs(np.array(self.data_fit_line.best_fit) - mid_value)).argmin()
        self.fifty_percent_val = self.x_fit_range[index]
        print("\n\n50% Method:")
        print("Tc = ", np.round(self.fifty_percent_val,3))
        
    def write_file(self):
        with open(self.txt_file, "a") as myfile:
            myfile.write("\n\n\n====================================\nChannel :" + str(self.channel))
            myfile.write("\nOnset/Endpoint Method:\n")
            myfile.write(str(np.round(self.onset,3)) + " <= Tc <= " + str(np.round(self.endpoint,3)))
            myfile.write("\ndeltaTc = " + str(np.round(self.endpoint - self.onset,3)))
            
            myfile.write("\n\n90/10 Method:\n")
            myfile.write(str(np.round(self.tc_10,3))+ " <= Tc <= " + str(np.round(self.tc_90,3)))
            myfile.write("\ndeltaTc = " + str(np.round(self.tc_90 - self.tc_10,3)))
            
            myfile.write("\n\nGaussian Inflection Point Method:\n")
            if(~self.gfail):
                myfile.write(str(np.round(self.tc_gauss_low,3)) + " <= Tc <= " + str(np.round(self.tc_gauss_high,3)))
                myfile.write("\ndelatTc = " + str(np.round(self.tc_gauss_high - self.tc_gauss_low,3)))
            else:
                myfile.write("\nFailure in Gassian Inflection Calculation")
            
            myfile.write("\n\nX-Intercept Method:\n")
            if(~self.xfail):
                myfile.write("Tc = " + str(np.round(self.tc_x_int,3)))
            else:
                myfile.write("\nFailure in x intercept Calculation")

            
            myfile.write("\n\n50% Method:\n")
            myfile.write("Tc = " + str( np.round(self.fifty_percent_val,3)))



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
    test = determine_tc(temp, res,1,"text.txt", "graph.png")
    test.calc_all()


