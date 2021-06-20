# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 17:46:51 2021

@author: jakes
"""

class Chlorophyll():
    
    """
    This is the light-gathering stage of photosynthesis
    """
    
    def __init__(self, peak, maxEfficiency): ## Later add a wavelength-dependent efficiency profile
        # This will require changes to the Conditions module as well to build in wavelength
        self.peak = peak
        self.maxEfficiency = maxEfficiency # of photosynthesis
        
    def getPeak(self):
        return self.peak
    
    def getEfficiency(self): # Could later become wavelength independent
        return self.maxEfficiency
    
    def absorbLight(self, energyDensity): # this is still an energy density
        
        absorptionDensity = energyDensity * self.getEfficiency()

        return absorptionDensity

    def lightHeating(self, energyDensity):
        pass # From non-absorbed light
        
        
    
class Membrane(): # Again, done per surface area for later implementation
    
    """ 
    Exchange of substances occurs here, created for possible future functionality
    """
    
    def __init__(self):
        pass
    
    def outwards(self, outwardsFlux):
        pass # e.g. could be used with a permeability function, giving classes to each possible substance
    
        # Could be called once per cycle by the chloroplast to respond to gradients set up by photosynthesis accordingly
    def inwards(self, inwardsFlux):
        pass
    


class GlucoseProductionSystem(): # Glucose produced per chloroplast surface area, i.e. NO PENETRATION
    
    """
    This will produce the glucose from a given fixed energy
    """
    
    def __init__(self, glucEff):
        self.glucEff = glucEff
        self.proportions = {"CO2":6.0, "Light":4.75E-18, "H2O":6} # Proportions of required reactants, light energy based of Gibbs free energy per glucose formed
        
    def getEff(self):
        return self.glucEff
    
    def getProp(self):
        return self.proportions
        
    def controlReactants(self, CO2, energyDensity, H2O): # O2 can be included later if it has an efficiency impact
        props = self.getProp()    
        
        CO2Ratio = CO2 / props["CO2"]
        lightRatio = energyDensity / props["Light"]
        H2ORatio = H2O / props["H2O"]
        
        # Figure out what to return and finish programming reaction flow
    


class Chloroplasts(): # This will incorporate all the functionality
    
    """
    REDO FOR A SPHERICAL CHLOROPLAST WITH A RADIUS PARAMETER"""

    """
    Made OUT OF chlorophyll, one per cell in algae
    """
    
    def __init__(self, area):
        self.area = area
        self.objChlorophyll = Chlorophyll()
        
    def getArea(self):
        return self.area
    
    def useChloro(self):
        return self.objChlorophyll
    
    def totalLight(self, energyDensity):
        absorptionDensity = self.useChloro().absorbLight(energyDensity)
        absorbed = self.getArea() * absorptionDensity
        
        return absorbed
    

        
        
        
        
        