#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:02:15 2016

@author: carlos
"""

import GA as ga
import random as random
import SYSTEMMODEL as systemmodel


n_nodes=200
system = systemmodel.SYSTEMMODEL()
system.configurationB(nodes=n_nodes)

g = ga.GA(system)
g.generatePopulation(g.populationPt)


numberofGenerations = 10


paretoResults = []
paretoGeneration=g.populationPt.paretoExport()
paretoResults.append(paretoGeneration)

for i in range(numberofGenerations):
    
    #g.evolveNGSA2()
    print "[Offsrping generation]: Generation number %i **********************" % i 
    paretoGeneration=g.populationPt.paretoExport()
    paretoResults.append(paretoGeneration)



#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    