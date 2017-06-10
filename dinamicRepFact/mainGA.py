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
import copy as copy



for n_nodes in [8,16,32]:

    #SI HAY QUE METER UN BUCLE CON DISTINTOS CASOS EMPEZARÍA AQUI
    
    #n_nodes=8 #DEBE DE SER DIVISIBLE POR 4 (numero racks) Y POR 8 tipos de máquinas
    system = systemmodel.SYSTEMMODEL()
    system.configurationMORM(nodes=n_nodes)
    
    g = ga.GA(system)
    
    g.HadoopRulesCreation = True
    g.BalanceObjective = False
    g.HardMutation = True
    g.AveregaObjectives = True
    
    system.initialAllocation=g.getRandomChromosome()
    
    
    g.generatePopulation(g.populationPt)
    
    
    
    startingpopulation = copy.deepcopy(g.populationPt.population)
    startingfitness = copy.deepcopy(g.populationPt.fitness)
    startingdominatesTo = copy.deepcopy(g.populationPt.dominatesTo)
    startingdominatedBy = copy.deepcopy(g.populationPt.dominatedBy)
    startingfronts = copy.deepcopy(g.populationPt.fronts)
    startingcrowdingDistances = copy.deepcopy(g.populationPt.crowdingDistances)
    startingnodesUsages = copy.deepcopy(g.populationPt.nodesUsages)
    
    numberofGenerations = 50
    
    
    configuration = []
    configuration.append(['OBJECTIVE','DYNAMIC','OURNET'])
    configuration.append(['OBJECTIVE','STATIC','OURNET'])
    configuration.append(['OBJECTIVE','DYNAMIC','BADNET'])
    configuration.append(['OBJECTIVE','STATIC','BADNET'])
    
    
    #for g.Migration in ['OBJECTIVE','NSGA']:
    #for g.Migration in ['OBJECTIVE']:
    #    for g.replicaFactor in ['DYNAMIC', 'STATIC']:
    #        for g.networkType in ['OURNET', 'BADNET']:
    #        for g.networkType in ['OURNET', 'BADNET']:
    
    for repetition in configuration:            
                
        g.Migration = repetition[0]
        g.replicaFactor = repetition[1]
        g.networkType = repetition[2]
        
        res = results.RESULTS()
        res.initDataCalculation()
        #g.Migration = 'OBJECTIVE' # OBJECTIVE or NSGA
        
        res.idString = str(n_nodes) + g.Migration + g.replicaFactor + g.networkType
    
        g.populationPt.population = copy.deepcopy(startingpopulation)
        g.populationPt.fitness = copy.deepcopy(startingfitness)
        g.populationPt.dominatesTo = copy.deepcopy(startingdominatesTo)
        g.populationPt.dominatedBy = copy.deepcopy(startingdominatedBy)
        g.populationPt.fronts = copy.deepcopy(startingfronts)
        g.populationPt.crowdingDistances = copy.deepcopy(startingcrowdingDistances)
        g.populationPt.nodesUsages = copy.deepcopy(startingnodesUsages)            
        
        if g.networkType == 'BADNET':
            g.calculateSolutionsWorkload(g.populationPt)
            g.calculatePopulationFitnessObjectives(g.populationPt)
            g.fastNonDominatedSort(g.populationPt)
    
            
        
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
        res.storeCSV(str(n_nodes) + g.Migration+'.'+g.replicaFactor + '.' + g.networkType)
    #    res.storeData(paretoResults,"allgenerations")
        res.storeData(paretoGeneration,"lastgeneration")
    
        res.closeCSVs()
        
     #   res.plotparetoEvolution(paretoResults,1)
        
        dataSerie = [res.network,res.reliability,res.migration,res.nodeNumber,res.replicaNumber]
        title = ['Network','Reliability','Migration','Node number', 'Replica number']
        ylabel = ['Time units (t)','Fail rate (1/t)','Time units (t)','Node number','Replica number']
        seriesToPlot = ['mean','min','single']
        minYaxes = [None,None,None,None,None]
        
        res.plotfitEvolution(dataSerie,title,ylabel,seriesToPlot,minYaxes)
        
        
        res.storeData(dataSerie,"fitevolutions")
    
    
        


#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    