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
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt3d


class RESULTS:
    

    def __init__(self):
        
        
        self.executionId= datetime.now().strftime('%Y%m%d%H%M%S')
        self.file_path = "./"+self.executionId
        
        self.idString = ''
        
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        
        self.outputCSV = open(self.file_path+'/execution_data.csv', 'wb')
        self.outputLOG = open(self.file_path+'/log.txt', 'wb')

        strTitle = "config;maxbalance;minbalance;meanbalance;singlebalance;maxnetwork;minnetwork;meannetwork;singlenetwork;maxreliability;minreliability;meanreliability;singlereliability;maxmigration;minmigration;meanmigration;singlemigration;maxnodeNumber;minnodeNumber;meannodeNumber;singlenodeNumber;maxreplicaNumber;minreplicaNumber;meanreplicaNumber;singlereplicaNumber"
        self.outputCSV.write(strTitle)
        self.outputCSV.write("\n")

    def storeCSV(self,strConfig):
        
        strCSV = strConfig +';'+ str(self.balanceuse['max'][-1])+';'+str(self.balanceuse['min'][-1])+';'+str(self.balanceuse['mean'][-1])+';'+str(self.balanceuse['sfit'][-1])+';'+ str(self.network['max'][-1])+';'+str(self.network['min'][-1])+';'+str(self.network['mean'][-1])+';'+str(self.network['sfit'][-1])+';'+ str(self.reliability['max'][-1])+';'+str(self.reliability['min'][-1])+';'+str(self.reliability['mean'][-1])+';'+str(self.reliability['sfit'][-1])+';'+ str(self.migration['max'][-1])+';'+str(self.migration['min'][-1])+';'+str(self.migration['mean'][-1])+';'+str(self.migration['sfit'][-1])+';'+ str(self.nodeNumber['max'][-1])+';'+str(self.nodeNumber['min'][-1])+';'+str(self.nodeNumber['mean'][-1])+';'+str(self.nodeNumber['sfit'][-1])+';'+ str(self.replicaNumber['max'][-1])+';'+str(self.replicaNumber['min'][-1])+';'+str(self.replicaNumber['mean'][-1])+';'+str(self.replicaNumber['sfit'][-1])
        self.outputCSV.write(strCSV)
        self.outputCSV.write("\n")
        
    def storeData(self,paretoResults,datatype):
        
        output = open(self.file_path+'/'+self.idString+datatype+'.pkl', 'wb')
        pickle.dump(paretoResults, output)
        output.close()

    def closeCSVs(self):
        self.outputCSV.close()
        self.outputLOG.close()

        
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


        self.migration={}
        self.migration['min'] = []
        self.migration['max'] = []
        self.migration['mean'] = []
        self.migration['sfit'] = []


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
        mylen=0
        for i in solution:
            mylen += len(set(solution[i]['rnode']+solution[i]['wnode']))
        return mylen
        
    def calculateNodeNumber(self, nodesUsages):       
        nodenum=0
        for i in nodesUsages:
            if i['cpuload'] > 0.0 or i['hdsize'] > 0.0:
                nodenum +=1
        return nodenum
        
        
        
    def calculateOneGenerationData(self,paretoGeneration,BalanceObjective):
        
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
        else:
            self.balanceuse['min'].append(-1)
            self.balanceuse['max'].append(-1)
            self.balanceuse['mean'].append(-1)
            self.balanceuse['sfit'].append(-1) 
        
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

        
        seqmig = [x['migration'] for x in paretoGeneration.fitness if len(x)>0]

        mmin = min(seqmig)
        mmax = max(seqmig)
        self.migration['min'].append(mmin)
        self.migration['max'].append(mmax)
        self.migration['mean'].append(np.mean(seqmig))            

      
        if BalanceObjective:
            balDiff = bmax - bmin
        netDiff = nmax - nmin
        relDiff = rmax - rmin
        migDiff = mmax - mmin

#            seqfit = [ ( math.pow(((x['balanceuse']-bmin)/(balDiff))*(1.0/3.0),2) + math.pow(((x['network']-nmin)/(netDiff))*(1.0/3.0),2) + math.pow(((x['reliability']-rmin)/(relDiff))*(1.0/3.0),2) )  for x in paretoGeneration.fitness if len(x)>0]

        if BalanceObjective:
            myWeight = 4.0
        else:
            myWeight = 3.0
        seqfit = []
        for x in paretoGeneration.fitness:
            if len(x)>0:
                if BalanceObjective:
                    if (balDiff) > 0:
                        balValue= ((x['balanceuse']-bmin)/(balDiff))*(1.0/myWeight)
                    else:
                        balValue = 1.0*(1.0/myWeight)
                if (netDiff) > 0:
                    netValue = ((x['network']-nmin)/(netDiff))*(1.0/myWeight)
                else:
                    netValue = 1.0*(1.0/myWeight)
                if (relDiff) > 0:
                    relValue = ((x['reliability']-rmin)/(relDiff))*(1.0/myWeight)
                else:
                    relValue = 1.0*(1.0/myWeight)
                if (migDiff) > 0:
                    migValue = ((x['migration']-mmin)/(migDiff))*(1.0/myWeight)
                else:
                    relValue = 1.0*(1.0/myWeight)                    
                if BalanceObjective:
                    seqfit.append(balValue+netValue+relValue+migValue)
                else:
                    seqfit.append(netValue+relValue+migValue)
                
                   
                   
        self.fitness['min'].append(min(seqfit))
        self.fitness['max'].append(max(seqfit))
        self.fitness['mean'].append(np.mean(seqfit))
        
        smallerFitIndex = seqfit.index(min(seqfit))

        
        
        self.replicaNumber['sfit'].append(seqchu[smallerFitIndex])   
        self.nodeNumber['sfit'].append(seqnode[smallerFitIndex]) 
        if BalanceObjective:               
            self.balanceuse['sfit'].append(seqbal[smallerFitIndex])
        self.migration['sfit'].append(seqmig[smallerFitIndex])  
        self.reliability['sfit'].append(seqrel[smallerFitIndex])  
        self.network['sfit'].append(seqnet[smallerFitIndex])     


            
    def calculateAllData(self,paretoResults,BalanceObjective):

    
    
        for paretoGeneration in paretoResults:
#TODO        
            self.calculateOneGenerationData(paretoGeneration,BalanceObjective)          
             
     
    def plotOneParetoEvolution(self,paretoGeneration,generationNum):
        font = {'size'   : 10}

        matplotlib.rc('font', **font)
        
        fig = plt.figure()
        fig.suptitle("Generation "+str(generationNum), fontsize=18)
        ax = fig.add_subplot(111, projection='3d')
        plt.gcf().subplots_adjust(left=0.00)

    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        #### quitarlo para que no sea solo el frente pareto 
        #### while len(popT.fronts[f])!=0:
        thisfront = [paretoGeneration.fitness[i] for i in paretoGeneration.fronts[0]]

        a = [thisfront[i]["network"] for i,v in enumerate(thisfront)]
        b = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]
        c = [thisfront[i]["migration"] for i,v in enumerate(thisfront)]


        ax.scatter(a, b, c, color='blue', marker="o")

        ax.set_xlabel('network', fontsize=18)
        ax.set_ylabel('reliability', fontsize=18)
        ax.set_zlabel('migration', fontsize=18,rotation=90)
    
        fig.savefig(self.file_path+'/pareto-gen'+str(generationNum)+'.pdf')
        plt.close(fig)
            

    def plotparetoEvolution(self,paretoResults,generationInterval):

        font = {'size'   : 10}

        matplotlib.rc('font', **font)

        
        for generationNum in range(0,len(paretoResults),generationInterval):
            self.plotOneParetoEvolution(paretoResults[generationNum],generationNum)
            
            
        
    def plotfitEvolution(self,dataSerie,title,ylabel,seriesToPlot,minYaxes):
        
        font = {'size'   : 18}

        matplotlib.rc('font', **font)
        
        for plotId in range(0,len(dataSerie)):
        
            figtitleStr = title[plotId]

            mydataSerie = dataSerie[plotId]

                
        #ejemplo sacado de http://matplotlib.org/users/text_intro.html    
            fig = plt.figure()
       #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
            fig.suptitle(figtitleStr, fontsize=18)
            ax = fig.add_subplot(111)
            fig.subplots_adjust(bottom=0.15)
       #    ax.set_title('axes title')
            ax.set_xlabel('Generations', fontsize=18)
            ax.set_ylabel(ylabel[plotId], fontsize=18)
            plt.gcf().subplots_adjust(left=0.18)
            plt.gcf().subplots_adjust(right=0.95)
            
            
            if 'max' in seriesToPlot:
                ax.plot(mydataSerie['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=30)
            if 'mean' in seriesToPlot:    
                ax.plot(mydataSerie['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=30)
            if 'min' in seriesToPlot:
                ax.plot(mydataSerie['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=30)
            if 'single' in seriesToPlot:
                ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=30)    
            plt.legend(loc="upper center", ncol=3, fontsize=14) 
        #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
            #plt.legend()
       #    plt.show()
            if minYaxes[plotId]!= None:
                plt.ylim(ymin=minYaxes[plotId])
       
       
            plt.grid()
            fig.savefig(self.file_path+'/'+self.idString+title[plotId].replace(" ", "")+'.pdf')
            plt.close(fig)

    
   
