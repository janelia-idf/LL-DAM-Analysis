# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 12:19:53 2016

@author: laughreyl
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt

x=np.linspace(-2*np.pi, 2*np.pi)
y1 = np.sin(x)
y2 = np.sin(x)
 
fig, axes = plt.subplots(1,2)       # creates frames 
axes[0].plot(x,y1,                  # draws the line
            color='r',              
# or hex:  
#            color='#ff0080',
            linewidth=5,
            linestyle='--'
            )                  
            
plt.sca(axes[0])
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],['-pi', '-pi/2', '0', 'pi/2', 'pi']
            label = 'my_label'
            )
plt.yticks




 axes[1].plot(x,y2)






