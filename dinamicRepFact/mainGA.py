#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:02:15 2016

@author: carlos
"""

import GA as ga
import random as random
import SYSTEMMODEL as systemmodel
import RESULTS as results





#SI HAY QUE METER UN BUCLE CON DISTINTOS CASOS EMPEZARÍA AQUI

n_nodes=8
system = systemmodel.SYSTEMMODEL()
system.configurationMORM(nodes=n_nodes)

g = ga.GA(system)

g.HadoopRulesCreation = True
g.BalanceObjective = False
g.HardMutation = True

system.initialAllocation=g.getRandomChromosome()

numberofGenerations = 200

for g.Migration in ['OBJECTIVE','NSGA']:
    res = results.RESULTS()
    res.initDataCalculation()
    #g.Migration = 'OBJECTIVE' # OBJECTIVE or NSGA
    g.generatePopulation(g.populationPt)
    res.idString = g.Migration
    
    
    paretoResults = []
    paretoGeneration=g.populationPt.paretoExport()
    paretoResults.append(paretoGeneration)
    
    res.calculateOneGenerationData(paretoGeneration,g.BalanceObjective)
    
    for i in range(numberofGenerations):
        
        g.evolveNGSA2()
        print("[Offsrping generation]: Generation number "+str(i)+" **********************\n")
        res.outputLOG.write("[Offsrping generation]: Generation number "+str(i)+" **********************\n")
        res.outputLOG.flush()
        paretoGeneration=g.populationPt.paretoExport()
#        paretoResults.append(paretoGeneration)
        res.plotOneParetoEvolution(paretoGeneration,i+1)
        res.calculateOneGenerationData(paretoGeneration,g.BalanceObjective)
    
#    res.calculateAllData(paretoResults,g.BalanceObjective)
    res.storeCSV(g.Migration)
#    res.storeData(paretoResults,"allgenerations")
    res.storeData(paretoGeneration,"lastgeneration")

    res.closeCSVs()
    
    #res.plotparetoEvolution(paretoResults,1)
    
    dataSerie = [res.network,res.reliability,res.migration,res.nodeNumber,res.replicaNumber]
    title = ['Network','Reliability','Migration','Node number', 'Replica number']
    ylabel = ['Time units (t)','Fail rate (1/t)','Time units (t)','Node number','Replica number']
    seriesToPlot = ['mean','min','single']
    minYaxes = [0,0,0,0,0]
    
    res.plotfitEvoluation(dataSerie,title,ylabel,seriesToPlot,minYaxes)
    
    
    res.storeData(dataSerie,"fitevolutions")


    


#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    