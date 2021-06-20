# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 21:08:29 2021

@author: jakes
"""

class Flow():
    
    def __init__(self, fieldsIn, fieldsOut, rules): # fields should be in the same order as their functional relations
        # if multiple fields per rule, the fields should be grouped into interior lists
        self.fin = fieldsIn
        self.fout = fieldsOut
        self.rules = rules # This holds the relationships between fields as a list of callable functions
        # Eventual rules can contain conditionals, etc...
        
    def getFin(self):
        return self.fin
    
    def getFout(self):
        return self.fout
    
    def getRules(self):
        return self.rules
    
    def act(self): 
    
        fin = self.getFin()
        fout = self.getFout()
        rules = self.getRules()
    
        for i in range(len(rules)):
            function = rules[i]
            function(fin[i], fout[i])
    
        
    
    