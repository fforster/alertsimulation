import numpy as np
import matplotlib.pyplot as plt

# variable class
class variableclass(object):

    # initialize object
    def __init__(self, **kwargs):
        
        # labels and colors
        self.label = kwargs["label"]
        self.color = kwargs["color"]

        # inherit N0 and invtau from another object
        if "obj" in kwargs.keys():
            obj = kwargs["obj"]
            self.N0 = obj.N0
            self.invtau = obj.invtau
        else:
            # use new values
            self.N0 = [kwargs["N0"]] # [alerts/day]
            if "invtau" in kwargs.keys():
                self.invtau = [kwargs["invtau"]] # [alerts/day]
            else:
                self.invtau = [-np.log(kwargs["N1"] / self.N0[-1]) / kwargs["t1"]]      
                    
    # add component
    def addcomponent(self, **kwargs):

        # inherit from another object
        if "obj" in kwargs.keys():
            obj = kwargs["obj"]
            self.N0 = self.N0 + obj.N0 # + joins lists
            self.invtau = self.invtau + obj.invtau
        else:
            self.N0.append(kwargs["N0"]) # [alerts/day]
            if "invtau" in kwargs.keys():
                self.invtau.append(kwargs["invtau"]) # [alerts/day]
            else:
                self.invtau.append(-np.log(kwargs["N1"] / self.N0[-1]) / kwargs["t1"])

    # compute rate of alerts from new objects, time in yr
    def doratenew(self, t):
        
        rate = 0
        for N0, invtau in zip(self.N0, self.invtau):
            rate += N0 * np.exp(-t * invtau)
        return rate
       
    # cumulative rate for all alerts, time in yr
    def documulativeall(self, t):
        
        yr = 365.25 # yr in days
        return np.sum(self.N0) * yr * t
       
    # compute cumulative for new alerts (objects), time in yr
    def documulativenew(self, t):
        
        yr = 365.25 # yr in days
        cum = 0
        for N0, invtau in zip(self.N0, self.invtau):
            if invtau != 0:
                cum += N0 / invtau * yr * (1. - np.exp(-t * invtau))
            else:
                cum += N0 * yr * t
        return cum
    
    # probability of an alert corresponding a new object, time in years
    def probnew(self, t):
        
        return self.documulativenew(t) / self.documulativeall(t)
    
    # probability of alert from object in cache of given size
    def probobjincache(self, t, cachesize):
        
        return np.minimum(1., cachesize / self.documulativenew(t))
    

    # size of annotation batch if annotation takes a given time (annnotationtime in seconds, time in years)
    def annotationbatchsize(self, t, annotationtime):

        # nbatch / annotationtime = rate new of objects
        return self.doratenew(t) * (annotationtime / (24. * 60 * 60.))
