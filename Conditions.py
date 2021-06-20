# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:50:21 2021

@author: jakes

This module defines the environmental conditions surrounding the algae

"""

import numpy as np

class waterBody():
    
    """ 
    This class makes up the entirety of the algal habitat, and is divided into
    cells, each with discrete values for important components
    """
    
    def __init__(self):
        self.cells = np.empty((10, 10), dtype = np.ndarray)
        self.components = ["CO2", "Light", "O2", "H2O", "Nutrients"] # Sort of extraneous
        
    def getCells(self):
        return self.cells
    
    def setCells(self, newCells):
        self.cells = newCells
    
    def getComponents(self):
        return self.components
    
    def setCO2(self, level):
        return level
    
    def setLight(self, level):
        return level
    
    def setO2(self, level):
        return level
    
    def setH2O(self, level):
        return level
    
    def setNutrients(self, level):
        return level
    
    
    def populateCells(self):
        cO2 = self.setCO2(0.3) ## ppm
        light = self.setLight(50) ## joule/m^2
        O2 = self.setO2(1.0) ## ppm
        H2O = self.setH2O(1) ## Decide unit later
        nutrients = self.setNutrients(0.5) # 0-1 scale 
        

        cells = self.getCells()
        cellShape = cells.shape
        
        cellConditions = np.array([cO2, light, O2, H2O, nutrients]) # Can be made more complex for gradients or random values
        
        
        for i in range(cellShape[0]):
            for j in range(cellShape[1]):
                cells[i][j] = cellConditions
                
        self.setCells(cells)
        
if __name__ == "__main__":
    pond = waterBody()
    # print (pond.getCells())  
    pond.populateCells()
    # print (pond.getCells())        
        
        
        
        
        
    