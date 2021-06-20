# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 21:11:45 2021

@author: jakes
"""

import numpy as np
import ScalarField as sf
import Flows as fl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def twoFieldRule(fieldIn, fieldOut):
    
    fieldIn.setLimitDivergences()
    fieldOut.updateIdealDivergences(-1 * fieldIn.getDivergences(), True)
    fieldOut.setLimitDivergences()
    
    
# System initialisation -----------------

fieldVal = np.full((10, 10), 10)

field1 = sf.ScalarField(fieldVal)
field2 = sf.ScalarField(fieldVal)

interactionMatrix = np.zeros((10, 10))

maxFlow = 0.5 # this is a ~positive~ flow

interactionMatrix[4][4] = maxFlow
interactionMatrix[4][5] = maxFlow
interactionMatrix[5][4] = maxFlow
interactionMatrix[5][5] = maxFlow

field1.updateIdealDivergences(-1 * interactionMatrix, True)

flow = fl.Flow([field1], [field2], [twoFieldRule])

# -----------------------------------------

# System running --------------------------


timesteps = 5000
    
results1 = []
results2 = []
    
for t in range(timesteps):
    if t % 10 == 0:
        if t % 50 == 0:
            results1.append(field1.getValues())
            results2.append(field2.getValues())
            print (t / 50)
        field1.diffuse()
        field2.diffuse()
        flow.act()
        field1.applyDivergences()
        field2.applyDivergences()
        
def animate1(i):
    result1 = results1[i]
    plt.contourf(result1, 200)
    plt.clim(vmin = 0, vmax = 20)

def animate2(i):
    result2 = results2[i]
    plt.contourf(result2, 200)
    plt.clim(vmin = 0, vmax = 20)



print ('Field 1:')
print (results1[0])
print (field1.getValues())
print ()
print ('Field 2:')
print (results2[0])
print (field2.getValues())
      
fig = plt.figure()
plt.title(f'Diffusive Field 1, t = 0 -> {timesteps}')
ax = plt.axes()
plt.xlim(0, 9)
plt.ylim(0, 9)
plt.xlabel(r'x')
plt.ylabel(r'y')

ani1 = animation.FuncAnimation(fig, animate1, frames = 99, repeat = False)
ani1.save('field1.gif')


fig = plt.figure()
plt.title(f'Diffusive Field 2, t = 0 -> {timesteps}')
ax = plt.axes()
plt.xlim(0, 9)
plt.ylim(0, 9)
plt.xlabel(r'x')
plt.ylabel(r'y')

ani2 = animation.FuncAnimation(fig, animate2, frames = 99, repeat = False)
ani2.save('field2.gif')  
    







