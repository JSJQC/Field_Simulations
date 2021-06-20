# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:31:19 2021

@author: jakes
"""

import numpy as np
import ScalarField as sf
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

fieldVal = np.full((6, 6), 10)

field1 = sf.ScalarField(fieldVal)
field2 = sf.ScalarField(fieldVal)

# Create the matrix defining the flow between the fields

interactionMatrix = np.zeros((6, 6))

maxFlow = 0.5 # this is a ~positive~ flow

interactionMatrix[2][2] = maxFlow
interactionMatrix[2][3] = maxFlow
interactionMatrix[3][2] = maxFlow
interactionMatrix[3][3] = maxFlow

print (interactionMatrix)

# define flow out of field1

field1.updateIdealDivergences(-1 * interactionMatrix, True)

timesteps = 1000
    
results1 = []
results2 = []
    
for t in range(timesteps):
    if t % 10 == 0:
        results1.append(field1.getValues())
        results2.append(field2.getValues())
        print (t / 10)
        field1.iterate()
        field2.updateIdealDivergences(-1 * field1.getDivergences(), True)
        field2.iterate()
    
    
def animate1(i):
    result1 = results1[i]
    plt.contourf(result1, 100)
    plt.clim(vmin = 0, vmax = 98)

def animate2(i):
    result2 = results2[i]
    plt.contourf(result2, 100)
    plt.clim(vmin = 0, vmax = 98)
 
'''       
fig = plt.figure()
plt.title(f'Diffusive Field, t = 0 -> {timesteps}')
ax = plt.axes()
plt.xlim(0, 49)
plt.ylim(0, 49)
plt.xlabel(r'x')
plt.ylabel(r'y')
        

ani1 = animation.FuncAnimation(fig, animate1, frames = 98, repeat = False)
ani1.save('field1.gif')
ani2 = animation.FuncAnimation(fig, animate2, frames = 98, repeat = False)
ani2.save('field1.gif')  

fig = plt.figure()
plt.title('1, t = 0')
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel(r'x')
plt.ylabel(r'y')

plt.contourf(results1[0], 50)
plt.clim(vmin = 0, vmax = 10)
plt.colorbar()
plt.show()

fig = plt.figure()
plt.title(f'1, t = {timesteps}')
ax = plt.axes()
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel(r'x')
plt.ylabel(r'y')

plt.contourf(results1[99], 50)
plt.clim(vmin = 0)
plt.colorbar()

plt.show()
'''
print ('Field 1:')
print (results1[0])
print (field1.getValues())
print ()
print ('Field 2:')
print (results2[0])
print (field2.getValues())

