# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:50:12 2018

@author: jlm7
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import matplotlib.animation as animation

from pylab import *
# plt.style.use('ggplot')
#
#def animate(i):
#    line.set_ydata(F[i, :])
#
#fig, ax = plt.subplots(figsize=(5, 3))
#ax.set(xlim=(-3, 3), ylim=(-1, 1))
#
#x = np.linspace(-3, 3, 91)
#t = np.linspace(1, 25, 30)
#X2, T2 = np.meshgrid(x, t)
# 
#sinT2 = np.sin(2*np.pi*T2/T2.max())
#F = 0.9*sinT2*np.sinc(X2*(1 + sinT2))
#
#line = ax.plot(x, F[0, :], color='k', lw=2)[0]
#
#anim = FuncAnimation(
#    fig, animate, interval=100, frames=len(t)-1)
#
#plt.draw()
#plt.show()



fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()