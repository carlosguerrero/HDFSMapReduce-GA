#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:02:15 2016

@author: carlos
"""

import GA as ga
import random as random



g = ga.GA()
g.generatePopulation()


numberofGenerations = 100

g.fastNonDominatedSort()
g.plotFronts()

g.crowdignDistancesAssigments(g.fronts[0])


     




#for i in range(numberofGenerations):
    #g.g.evolve()
    #print "[Offsrping generation]: Generation number %i **********************" % i 

#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    