# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 21:42:30 2021

@author: jakes
"""

import numpy as np
import ScalarField as sf
import Flows as fl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def threeFieldRule(fieldsIn, fieldOut):
    
    field1, field2 = [fieldsIn[i] for i in (0, 1)]
    field1.setLimitDivergences()
    field2.setLimitDivergences()
    fieldOut.updateIdealDivergences(-1 * field1.getDivergences(), True)
    fieldOut.updateIdealDivergences(-1 * field2.getDivergences())
    fieldOut.setLimitDivergences()
    
    
# System initialisation -----------------

fieldVal = np.full((6, 6), 10)

field1 = sf.ScalarField(fieldVal)
field2 = sf.ScalarField(fieldVal)
field3 = sf.ScalarField(fieldVal)

interactionMatrix = np.zeros((6, 6))

maxFlow = 0.5 # this is a ~positive~ flow

interactionMatrix[2][2] = maxFlow
interactionMatrix[2][3] = maxFlow
interactionMatrix[3][2] = maxFlow
interactionMatrix[3][3] = maxFlow

field1.updateIdealDivergences(-1 * interactionMatrix, True)
field2.updateIdealDivergences(-1 * interactionMatrix, True)

# Fields 1 and 2 flow identically into field 3

flow = fl.Flow([[field1, field2]], [field3], [threeFieldRule])

# -----------------------------------------

# System running --------------------------


timesteps = 100000
    
results1 = []
results2 = []
results3 = []
    
for t in range(timesteps):
    if t % 10 == 0:
        results1.append(field1.getValues())
        results2.append(field2.getValues())
        results3.append(field3.getValues())
        #print (t / 10)
        field1.diffuse()
        field2.diffuse()
        field3.diffuse()
        flow.act()
        field1.applyDivergences()
        field2.applyDivergences()
        field3.applyDivergences()
    
print ('Field 1:')
print (results1[0])
print (field1.getValues())
print ()
print ('Field 2:')
print (results2[0])
print (field2.getValues())
print ()
print ('Field 3:')
print (results3[0])
print (field3.getValues())






