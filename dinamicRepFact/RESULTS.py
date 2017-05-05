#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""

from datetime import datetime
import os
import numpy as np
import math

class RESULTS:
    

    def __init__(self):
        
        
        self.executionId= datetime.now().strftime('%Y%m%d%H%M%S')
        self.file_path = "./"+self.executionId
        
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        
        self.outputtotal = open(self.file_path+'/execution_data.csv', 'wb')

        
    def initDataCalculation(self):
        
        self.balanceuse={}
        self.balanceuse['min'] = []
        self.balanceuse['max'] = []
        self.balanceuse['mean'] = []
        self.balanceuse['sfit'] = []

        self.network={}
        self.network={}
        self.network['min'] = []
        self.network['max'] = []
        self.network['mean'] = []
        self.network['sfit'] = []


        self.reliability={}
        self.reliability['min'] = []
        self.reliability['max'] = []
        self.reliability['mean'] = []
        self.reliability['sfit'] = []


        self.nodeNumber={}
        self.nodeNumber['min'] = []
        self.nodeNumber['max'] = []
        self.nodeNumber['mean'] = []
        self.nodeNumber['sfit'] = [] 

        self.replicaNumber={}
        self.replicaNumber['min'] = []
        self.replicaNumber['max'] = []
        self.replicaNumber['mean'] = []
        self.replicaNumber['sfit'] = []


        self.fitness={}
        self.fitness['min'] = []
        self.fitness['max'] = []
        self.fitness['mean'] = []        

#TODO
    def calculateChunkReplicaNumber(self, solution):
        return 1
        
    def calculateNodeNumber(self, solution):        
        return 1
        
    def calculateData(self,paretoResults,BalanceObjective):
        netDiff = 1.0
        balDiff = 1.0
        relDiff = 1.0
    
    
        for paretoGeneration in paretoResults:
#TODO             
            seqchu = [self.calculateChunkReplicaNumber(x) for x in paretoGeneration.population if len(x)>0]
            cmin = min(seqchu)
            cmax = max(seqchu)
            self.replicaNumber['min'].append(cmin)
            self.replicaNumber['max'].append(cmax)
            self.replicaNumber['mean'].append(np.mean(seqchu))                   
#TODO            
            seqnode = [self.calculateNodeNumber(x) for x in paretoGeneration.nodesUsages if len(x)>0]
            pmin = min(seqnode)
            pmax = max(seqnode)
            self.nodeNumber['min'].append(pmin)
            self.nodeNumber['max'].append(pmax)
            self.nodeNumber['mean'].append(np.mean(seqnode))                   
    

            if BalanceObjective:            
                seqbal = [x['balanceuse'] for x in paretoGeneration.fitness if len(x)>0]
            
                bmin = min(seqbal)
                bmax = max(seqbal)
                self.balanceuse['min'].append(bmin)
                self.balanceuse['max'].append(bmax)
                self.balanceuse['mean'].append(np.mean(seqbal))
            
            
            seqnet = [x['network'] for x in paretoGeneration.fitness if len(x)>0]
        
            nmin = min(seqnet)
            nmax = max(seqnet)
            self.network['min'].append(nmin)
            self.network['max'].append(nmax)
            self.network['mean'].append(np.mean(seqnet))            
            
            
            seqrel = [x['reliability'] for x in paretoGeneration.fitness if len(x)>0]
        
            rmin = min(seqrel)
            rmax = max(seqrel)
            self.reliability['min'].append(rmin)
            self.reliability['max'].append(rmax)
            self.reliability['mean'].append(np.mean(seqrel))            
            
          
            if BalanceObjective:
                balDiff = bmax - bmin
            netDiff = nmax - nmin
            relDiff = rmax - rmin

#            seqfit = [ ( math.pow(((x['balanceuse']-bmin)/(balDiff))*(1.0/3.0),2) + math.pow(((x['network']-nmin)/(netDiff))*(1.0/3.0),2) + math.pow(((x['reliability']-rmin)/(relDiff))*(1.0/3.0),2) )  for x in paretoGeneration.fitness if len(x)>0]
    
            if BalanceObjective:
                myWeight = 3.0
            else:
                myWeight = 2.0
            seqfit = []
            for x in paretoGeneration.fitness:
                if len(x)>0:
                    if BalanceObjective:
                        if (balDiff) > 0:
                            balValue= math.pow(((x['balanceuse']-bmin)/(balDiff))*(1.0/3.0),2)
                        else:
                            balValue = 1.0*(1.0/3.0)
                    if (netDiff) > 0:
                        netValue = math.pow(((x['network']-nmin)/(netDiff))*(1.0/3.0),2)
                    else:
                        netValue = 1.0*(1.0/myWeight)
                    if (relDiff) > 0:
                        relValue = math.pow(((x['reliability']-rmin)/(relDiff))*(1.0/3.0),2)
                    else:
                        relValue = 1.0*(1.0/myWeight)
                    if BalanceObjective:
                        seqfit.append(balValue+netValue+relValue)
                    else:
                        seqfit.append(netValue+relValue)
                    
                       
                       
            self.fitness['min'].append(min(seqfit))
            self.fitness['max'].append(max(seqfit))
            self.fitness['mean'].append(np.mean(seqfit))
            
            smallerFitIndex = seqfit.index(min(seqfit))

            
            
            self.replicaNumber['sfit'].append(seqchu[smallerFitIndex])   
            self.nodeNumber['sfit'].append(seqnode[smallerFitIndex]) 
            if BalanceObjective:               
                self.balanceuse['sfit'].append(seqbal[smallerFitIndex])
            self.reliability['sfit'].append(seqrel[smallerFitIndex])  
            self.network['sfit'].append(seqnet[smallerFitIndex])      
     
            
     ######EL FITNESS NO SE CALCULA DE FORMA CORRECTA

        
        
    
   
