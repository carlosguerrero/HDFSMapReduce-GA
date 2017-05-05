#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""
import copy
import time

class POPULATION:
    
    def copyMyPopulation(self, pop):
        
        newPop = []
        for idSol,valSol in enumerate(pop):
            newSol = {}
            for idChunck,valChunck in valSol.iteritems():
                newSol[idChunck]= {'filetype': valChunck['filetype'], 'rnode': copy.copy(valChunck['rnode']), 'wnode': copy.copy(valChunck['wnode'])}
            newPop.append(newSol)
        return newPop
            
        
    
    def populationUnion(self,a,b):
        
        r=POPULATION(1)
        #tiempo1 = time.time()
        #tiempo2 = tiempo1
        #print "empezamos calculo copia"
        r.population = self.copyMyPopulation(a.population) + self.copyMyPopulation(b.population)
        
        #r.population = copy.deepcopy(a.population) + copy.deepcopy(b.population)
        
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar population:"+str(tiempo2-tiempo1)
        r.nodesUsages = copy.deepcopy(a.nodesUsages) + copy.deepcopy(b.nodesUsages)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar nodeusages:"+str(tiempo2-tiempo1)
        r.fitness = copy.deepcopy(a.fitness) + copy.deepcopy(b.fitness)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar fitness:"+str(tiempo2-tiempo1)
        for i,v in enumerate(r.fitness):
            r.fitness[i]["index"]=i
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de actualizar indices fitness:"+str(tiempo2-tiempo1)
        r.dominatesTo = copy.deepcopy(a.dominatesTo) + copy.deepcopy(b.dominatesTo)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar dominatesto:"+str(tiempo2-tiempo1)
        r.dominatedBy = copy.deepcopy(a.dominatedBy) + copy.deepcopy(b.dominatedBy)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar dominatedby:"+str(tiempo2-tiempo1)
        r.fronts = copy.deepcopy(a.fronts) + copy.deepcopy(b.fronts)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar fronts:"+str(tiempo2-tiempo1)
        r.crowdingDistances = copy.deepcopy(a.crowdingDistances) + copy.deepcopy(b.crowdingDistances)
        #tiempo1,tiempo2 = tiempo2,time.time()
        #print "Tiempo de copiar crowdistance:"+str(tiempo2-tiempo1)
        
        return r 
        
    def paretoExport(self):
        
        paretoPop = self.__class__(len(self.population))
        
        paretoPop.fronts[0] = copy.deepcopy(self.fronts[0])
        
        
        for i in paretoPop.fronts[0]:
            paretoPop.population[i] = copy.deepcopy(self.population[i])
            paretoPop.fitness[i] = copy.deepcopy(self.fitness[i])
            paretoPop.nodesUsages[i] = copy.deepcopy(self.nodesUsages[i])
            
        return paretoPop        

    def __init__(self,size):
        
        self.population = [{}]*size
        self.fitness = [{}]*size
        self.dominatesTo = [set()]*size
        self.dominatedBy = [set()]*size
        self.fronts = [set()]*size
        self.crowdingDistances = [float(0)]*size
        self.nodesUsages = [list()]*size
    
   
