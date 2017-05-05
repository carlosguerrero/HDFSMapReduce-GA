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



res = results.RESULTS()


#SI HAY QUE METER UN BUCLE CON DISTINTOS CASOS EMPEZARÍA AQUI

n_nodes=200
system = systemmodel.SYSTEMMODEL()
system.configurationB(nodes=n_nodes)
res.initDataCalculation()

g = ga.GA(system)

g.HadoopRulesCreation = True
g.BalanceObjective = False
g.HardMutation = True

g.generatePopulation(g.populationPt)


numberofGenerations = 100

paretoResults = []
paretoGeneration=g.populationPt.paretoExport()
paretoResults.append(paretoGeneration)

for i in range(numberofGenerations):
    
    g.evolveNGSA2()
    print "[Offsrping generation]: Generation number %i **********************" % i 
    paretoGeneration=g.populationPt.paretoExport()
    paretoResults.append(paretoGeneration)

res.calculateData(paretoResults,g.BalanceObjective)
    


#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    