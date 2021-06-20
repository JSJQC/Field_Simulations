# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:35:51 2021

@author: jakes

A module containing the attributes and methods of a generic scalar field
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

class ScalarField(): # 2D for now
    
    def __init__(self, initialValues): # Initial values should be a numpy array, could streamline this later
        self.D = 0.5 # Should be ~ 10E-11 for the real thing
        self.values = initialValues
        self.idealDivergences = np.zeros(initialValues.shape)
        self.divergences = np.zeros(initialValues.shape) # This is initialised as zero, same dimensions as the field itself
        
    def getValues(self):
        return self.values
    
    def setValues(self, new):
        self.values = new
    
    def getDivergences(self):
        return self.divergences
    
    def getIdealDivergences(self):
        return self.idealDivergences
    
    def setDivergences(self, new):
        self.divergences = new
        
    def setIdealDivergences(self, new):
        self.idealDivergences = new
        
    def updateDivergences(self, toAdd, reset = False): # toAdd must be same dimensions as the original dimensions
    # This will be used when adding new sources/sinks (ie. from reactions) to the field    
    
        if reset == True:
            self.setDivergences(toAdd)
        else:
            newDivergences = self.getDivergences() + toAdd
            self.setDivergences(newDivergences)
            
    def updateIdealDivergences(self, toAdd, reset = False): # toAdd must be same dimensions as the original dimensions
    # This will be used when adding new sources/sinks (ie. from reactions) to the field    
    
        if reset == True:
            self.setIdealDivergences(toAdd)
        else:
            newDivergences = self.getIdealDivergences() + toAdd
            self.setIdealDivergences(newDivergences)
        
    def setLimitDivergences(self): # produces a divergence field that will not overdrain the field
        # Should be implemented so that the draining field dictates the flowrate into the recieving field
        # Needs to be run every tick
        current = self.getValues()
        div = self.getIdealDivergences()
        newField = current + div
        dims = div.shape
        
        tweakFlag = False
        
        for i in range(dims[0]):
            for j in range(dims[1]):
                if newField[i][j] < 0:
                    newDiv = -1 * current[i][j]
                    div[i][j] = newDiv
                    tweakFlag = True
        
        self.updateDivergences(div, True)
        
    def applyDivergences(self): # Run each tick, like diffuse()
        self.setValues(self.getValues() + self.getDivergences())
    
    def calcGradient(self):
        newGradients = np.gradient(self.getValues())
        return newGradients
    
    def ficksField(self):
        #left edge, top edge > 0
        #right edge, bottom edge < 0 
        
        fluxy = -1 * self.D * self.calcGradient()[0]
        
        for i in range(len(fluxy[0])):
            if fluxy[0][i] < 0:
                fluxy[0][i] = 0.0
        
        for i in range(len(fluxy[-1])):
            if fluxy[-1][i] > 0:
                fluxy[-1][i] = 0.0
        
        
        fluxx = -1 * self.D * self.calcGradient()[1]
        
        for i in range(len(fluxx)):
            if fluxx[i][0] < 0:
                fluxx[i][0] = 0.0
                
            if fluxx[i][-1] > 0:
                fluxx[i][-1] = 0.0                
            
        
        return fluxy, fluxx
    
    def diffuse(self):
        oldVals = self.getValues()
        
        fluxy, fluxx = self.ficksField()
        
        diffOut = -1 * ( abs(fluxy) + abs(fluxx) )
        
        diffIn = np.zeros((len(fluxy), len(fluxx)))
        
        for i in range(len(fluxy)):
            for j in range(len(fluxy[i])):
                
                if i > 0:
                    above = fluxy[i-1][j]
                    
                    if above > 0:
                        diffIn[i][j] += abs(above)
                        
                if i < (len(fluxy) - 1):
                    below = fluxy[i+1][j]
                
                    if below < 0:
                        diffIn[i][j] += abs(below)
                        
                        
        for i in range(len(fluxx)):
            for j in range(len(fluxx[i])):
                
                if j > 0:
                    left = fluxx[i][j-1]
                    
                    if left > 0:
                        diffIn[i][j] += abs(left)
                        
                if j < (len(fluxx[i]) - 1):
                    right = fluxx[i][j+1]
                
                    if right < 0:
                        diffIn[i][j] += abs(right)
        
        
        newVals = oldVals + diffOut + diffIn
        
        self.setValues(newVals)
        
        
    def iterate(self): ## Constitues one cycle of the scalar field - add new functionality here

    # Think about the order of operations (ie. sources/sinks before diffusion?)

        self.diffuse()  
        self.setLimitDivergences()
        self.applyDivergences()
              
        
if __name__ == "__main__":
    
    
    systemy = 50
    systemx = 50
    
    ## left to right gradient ----------------------
    
    initialValues1 = np.empty((systemy,systemx))
    for i in range(systemy):
        for j in range(systemx):
            initialValues1[i][j] = j
            
    oneGradx = ScalarField(initialValues1)
    
    ## ---------------------------------------------
    
    ## top to bottom gradient ----------------------
    
    initialValues2 = np.empty((systemy,systemx))
    for i in range(systemy):
        for j in range(systemx):
            initialValues2[i][j] = i
            
    oneGrady = ScalarField(initialValues2)
    
    # print (oneGrady.ficksField())
    
    ## ---------------------------------------------
    
    ## top left to bottom right diagonal gradient --
    
    initialValues3 = np.empty((systemy,systemx))
    for i in range(systemy):
        for j in range(systemx):
            initialValues3[i][j] = i + j
            
    twoGrad = ScalarField(initialValues3)
    
    ## ---------------------------------------------
    
    # boundaryInflux is the divergence for a cell with a constant inflow of material over its surface (perimeter)
    boundaryInflux = np.zeros((systemy,systemx))
    for i in range(systemy):
        for j in range(systemx):
            if i == 0 or i == systemy - 1:
                boundaryInflux[i][j] = 2.0
            
            if j == 0 or j == systemx - 1:
                boundaryInflux[i][j] = 2.0
                
    #oneGradx.updateDivergences(boundaryInflux)
    #oneGrady.updateDivergences(boundaryInflux)
    #twoGrad.updateDivergences(boundaryInflux)
    
    timesteps = 1000
    
    results = []
    
    '''
    for t in range(timesteps):
        if t % 10 == 0:
            results.append(oneGradx.getValues())
        oneGradx.iterate()
    
    print (oneGradx.getValues())
    '''
    '''
    for t in range(timesteps):
        if t % 10 == 0:
            results.append(oneGrady.getValues())
        oneGrady.iterate()
    
    print (oneGrady.getValues())
    
    '''
    initialState = twoGrad.getValues()
    
    for t in range(timesteps):
        if t % 10 == 0:
            results.append(twoGrad.getValues())
            print (t / 10)
            # print (twoGrad.ficksField())
        twoGrad.iterate()
        
    #Writer = animation.writers['ffmpeg']
    #writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
    
    
    def animate(i):
        result = results[i]
        plt.contourf(result, 100)
        plt.clim(vmin = 0, vmax = 98)
        
    fig = plt.figure()
    plt.title(f'Diffusive Field, t = 0 -> {timesteps}')
    ax = plt.axes()
    plt.xlim(0, 49)
    plt.ylim(0, 49)
    plt.xlabel(r'x')
    plt.ylabel(r'y')
        
    ani = animation.FuncAnimation(fig, animate, frames = 98, repeat = False)
    ani.save('animation.gif')   
    
    
    fig = plt.figure()
    plt.title('[0]')
    plt.xlim(0, 49)
    plt.ylim(0, 49)
    plt.xlabel(r'x')
    plt.ylabel(r'y')
    
    plt.contourf(results[0], 100)
    plt.clim(vmin = 0, vmax = 98)
    plt.colorbar()
    plt.show()
    
    fig = plt.figure()
    plt.title('[1]')
    ax = plt.axes()
    plt.xlim(0, 49)
    plt.ylim(0, 49)
    plt.xlabel(r'x')
    plt.ylabel(r'y')
    
    plt.contourf(results[99], 100)
    plt.clim(vmin = 0, vmax = 98)
    plt.colorbar()
    
    plt.show()
    
    print (twoGrad.getValues())
    print ()
    print (initialState)
    

    # Fix the fact it all flows out the bottom of the system -- Done
    # Fix the colour plotting, then add an animated version to show diffusion
    # Fix the y-direction diffusion, then check with boundary y only boundary conditions -- Done
    # Begin to add the divergences/boundary conditions -- Done
        
        
        
        
        
        
        
        
    
    

