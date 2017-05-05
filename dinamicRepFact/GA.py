# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import numpy as np
import random as random
import sys
import matplotlib.pyplot as plt 
import matplotlib.cm as cm 
import POPULATION as pop
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt3d
import SYSTEMMODEL as systemmodel
import copy
import time



class GA:
    
    
    
    def __init__(self,system):
        
        self.system = system
#        self.nodenumber = 200
#        self.racknumber = 5 #el nodenumber ha de ser divisible por este numero
#        self.nodesXrack = self.nodenumber / self.racknumber

        self.populationSize = 100
        self.populationPt = pop.POPULATION(self.populationSize)
        self.mutationProbability = 0.30
        self.HadoopRulesCreation = True
        self.BalanceObjective = True
        self.HardMutation = False



#******************************************************************************************
#   MUTATIONS
#******************************************************************************************


    
    def hardMutate(self,child):

###        print "[Offsrping generation]: Mutation of blocks in process**********************" 

        
        for key,placement in child.iteritems():
            numReadBlocks = len(placement['rnode'])
            numWriteBlocks = len(placement['wnode'])

            mutationOperators = [] 
            if numReadBlocks>1:
                mutationOperators.append(self.swapTwoSchedulleMutation)
            if numWriteBlocks>0 and numReadBlocks>0:
                mutationOperators.append(self.swapBlockSchedulleMutation)
            if numReadBlocks>0:
                mutationOperators.append(self.changeSchedulleMutation)
            if numWriteBlocks>0:
                mutationOperators.append(self.changeBlockMutation)
            mutationOperators.append(self.addBlockMutation)
            if numWriteBlocks>0:
                mutationOperators.append(self.delBlockMutation)
            
            mutationOperators[random.randint(0,len(mutationOperators)-1)](placement)




    def swapTwoSchedulleMutation(self,blockDef): #swap the nodes where the MRjobs are schedulled for two MRjobs
#        print blockDef
        swapIdx = random.sample(range(0,len(blockDef['rnode'])),2)
        blockDef['rnode'][swapIdx[0]], blockDef['rnode'][swapIdx[1]] =  blockDef['rnode'][swapIdx[1]], blockDef['rnode'][swapIdx[0]]
#        print blockDef    
###        print "[Offsrping generation]: Swap Two Schedulled Mutation **********************"
        
    def swapBlockSchedulleMutation(self,blockDef): #swap the nodes where a MRjobs is schedulled with the node in which other copy of the block is stored
#        print blockDef
        schIdx = random.randint(0,len(blockDef['rnode'])-1)
        blckIdx = random.randint(0,len(blockDef['wnode'])-1)
        blockDef['rnode'][schIdx], blockDef['wnode'][blckIdx] =  blockDef['wnode'][blckIdx], blockDef['rnode'][schIdx]
#        print blockDef    
###        print "[Offsrping generation]: Swap Schedulle and Block Mutation **********************"
        
    def changeSchedulleMutation(self,blockDef): #alter the value of the nodes where a MRjob is schedulled
#        print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.system.nodenumber: 
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.system.nodenumber-1)
            schIdx = random.randint(0,len(blockDef['rnode'])-1)
            blockDef['rnode'][schIdx]=newNode
 #           print blockDef    
###            print "[Offsrping generation]: Change Schedulle Node Mutation **********************"
###        else:
###            print "[Offsrping generation]: Change Schedulle Node Mutation ERROR the block is stored in all the nodes **********************"
        
        
    def changeBlockMutation(self,blockDef): #alter the value of the nodes where a block is stored
#        print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.system.nodenumber: 
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.system.nodenumber-1)
            blckIdx = random.randint(0,len(blockDef['wnode'])-1)
            blockDef['wnode'][blckIdx]=newNode
#            print blockDef    
###            print "[Offsrping generation]: Change Block Node Mutation **********************"
###        else:
###            print "[Offsrping generation]: Change Block Node Mutation ERROR the block is stored in all the nodes **********************"
    
    
    def addBlockMutation(self,blockDef): #add a new node to store a replica of the block
 #       print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.system.nodenumber:
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.system.nodenumber-1)
            blockDef['wnode'].append(newNode)
#            print blockDef    
###            print "[Offsrping generation]: Add Block Mutation **********************"
###        else:
###            print "[Offsrping generation]: Add Block Mutation ERROR the block is stored in all the nodes **********************"
        
        
    def delBlockMutation(self,blockDef): #remove a node where a block replica is stored
#        print blockDef
        blckIdx = random.randint(0,len(blockDef['wnode'])-1)
        blockDef['wnode'].pop(blckIdx)
#        print blockDef    
###        print "[Offsrping generation]: Del Block Mutation **********************"
        
    
    def softMutate(self,child):
        blockSelected = random.randint(0,len(child)-1)
        blockSelectedKey = child.keys()[blockSelected]
###        print "[Offsrping generation]: Mutation of block %s in process**********************" % str(blockSelectedKey)
        numReadBlocks = len(child[blockSelectedKey]['rnode'])
        numWriteBlocks = len(child[blockSelectedKey]['wnode'])
        
        mutationOperators = [] 
        if numReadBlocks>1:
            mutationOperators.append(self.swapTwoSchedulleMutation)
        if numWriteBlocks>0 and numReadBlocks>0:
            mutationOperators.append(self.swapBlockSchedulleMutation)
        if numReadBlocks>0:
            mutationOperators.append(self.changeSchedulleMutation)
        if numWriteBlocks>0:
            mutationOperators.append(self.changeBlockMutation)
        mutationOperators.append(self.addBlockMutation)
        if numWriteBlocks>0:
            mutationOperators.append(self.delBlockMutation)
        
#        print mutationOperators
#        print "$$$$$$$$$$$$$$$"
    
#        mutationOperators = [] #simplificar esta formulación y considerar que readblocks sean 0
#        if numWriteBlocks>0 and numReadBlocks>1:  
#            mutationOperators.append(self.swapTwoSchedulleMutation)
#            mutationOperators.append(self.swapBlockSchedulleMutation)
#            mutationOperators.append(self.changeSchedulleMutation)
#            mutationOperators.append(self.changeBlockMutation)
#            mutationOperators.append(self.addBlockMutation)
#            mutationOperators.append(self.delBlockMutation)
#        elif not numWriteBlocks>0 and numReadBlocks>1:
#            mutationOperators.append(self.swapTwoSchedulleMutation)
#            #mutationOperators.append(self.swapBlockSchedulleMutation)
#            mutationOperators.append(self.changeSchedulleMutation)
#            #mutationOperators.append(self.changeBlockMutation)
#            mutationOperators.append(self.addBlockMutation)
#            #mutationOperators.append(self.delBlockMutation)
#        elif numWriteBlocks>0 and not numReadBlocks>1:
#            #smutationOperators.append(self.wapTwoSchedulleMutation)
#            mutationOperators.append(self.swapBlockSchedulleMutation)
#            mutationOperators.append(self.changeSchedulleMutation)
#            mutationOperators.append(self.changeBlockMutation)
#            mutationOperators.append(self.addBlockMutation)
#            mutationOperators.append(self.delBlockMutation)
#        elif not numWriteBlocks>0 and not numReadBlocks>1:
#            #mutationOperators.append(self.swapTwoSchedulleMutation)
#            #mutationOperators.append(self.swapBlockSchedulleMutation)
#            mutationOperators.append(self.changeSchedulleMutation)
#            #mutationOperators.append(self.changeBlockMutation)
#            mutationOperators.append(self.addBlockMutation)
#            #mutationOperators.append(self.delBlockMutation)
#        else:
#            print "[ERROR Mutation operation] a mutation cannot be done for blockKey "+ str(blockSelectedKey) + " and child " + str(child)
        mutationOperators[random.randint(0,len(mutationOperators)-1)](child[blockSelectedKey])
    

    def mutate(self,child):
        if self.HardMutation:
            self.hardMutate(child)
        else:
            self.softMutate(child)
        
        
        
#******************************************************************************************
#   END MUTATIONS
#******************************************************************************************



#******************************************************************************************
#   CROSSOVER
#******************************************************************************************


    def crossover(self,f1,f2,offs):
        c1 = f1.copy()
        c2 = f2.copy()
        #crossover of the write/block chromosome
        for key,value in c1.iteritems():
            setF1 = set(c1[key]['wnode'])
            setF2 = set(c2[key]['wnode'])
#            totalINI = len(c1[key]['wnode'])+len(c2[key]['wnode'])
            commonNodes = setF1 & setF2 # & es la intersección
            writeNodes = setF1 | setF2 # | es la union
#            print c1[key]['wnode']
#            print c2[key]['wnode']
            if len(writeNodes)<=1 and len(commonNodes)==0: #si solo hay uno, lo ponemos en ambos
                c1[key]['wnode']=list(writeNodes)
                c2[key]['wnode']=list(writeNodes)
            elif len(writeNodes)>1 and len(commonNodes)==0: #si hay mas de 2 y ninguno en comun, como minimo habrá uno en cada uno
                setC1 = set(random.sample(writeNodes,random.randint(1,len(writeNodes)-1)))
                setC2 = writeNodes-setC1
                c1[key]['wnode']=list(setC1 | commonNodes) # union de los comunes con los nuevos
                c2[key]['wnode']=list(setC2 | commonNodes)
            elif len(commonNodes)!=0: #si llegamos aquí es porque al menos hay uno en común, entonces los no comunes se pueden repartir sin un mínimo
                setC1 = set(random.sample(writeNodes,random.randint(0,len(writeNodes))))
                setC2 = writeNodes-setC1
                c1[key]['wnode']=list(setC1 | commonNodes) # union de los comunes con los nuevos
                c2[key]['wnode']=list(setC2 | commonNodes)                
            else:
                print "MEGAERROR"
                sys.exit(1)
#            totalFIN = len(c1[key]['wnode'])+len(c2[key]['wnode'])
#            if totalFIN != totalINI:
#                print "MEGAERROR"
#                sys.exit(1)
#            print c1[key]['wnode']
#            print c2[key]['wnode']
#            print "****"
        #crossover of the read/MRjobs chromosome
        for key,value in c1.iteritems():
#            print key
#            print c1[key]['rnode']
#            print c2[key]['rnode']
            for i in range(len(c1[key]['rnode'])):
                if random.uniform(0,1) > 0.5:
                    c1[key]['rnode'][i],c2[key]['rnode'][i] = c2[key]['rnode'][i],c1[key]['rnode'][i]
#            print c1[key]['rnode']
#            print c2[key]['rnode']
#            print "+++++"
        offs.append(c1)
###        print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
###        print "[Offsrping generation]: Children 2 added **********************"



#******************************************************************************************
#   END CROSSOVER
#******************************************************************************************

#******************************************************************************************
#   nodenumber calculation
#******************************************************************************************



    def calculateNodeNumber(self,solution):
        allNodes = set()
        for key in solution:
            allNodes = allNodes | set(solution[key]['rnode']+solution[key]['wnode'])
        
        return len(allNodes)


#******************************************************************************************
#   END nodenumber calculation
#******************************************************************************************



#******************************************************************************************
#   Cluster Balance use calculation
#******************************************************************************************



    def calculateClusterBalanceUse(self,nodesLoads):
        
        #nodesLoad.append({"cpuload" : 0.0, "memorysize": 0.0, "memoryload": 0.0, "hdsize": 0.0, "hdload": 0.0})

        cpuload = []
        memorysize = []
        memoryload = []
        hdsize = []
        hdload = []
        
        for idx,usage in enumerate(nodesLoads):
            #if usage['cpuload']>0.0 and usage['memoryload']>0.0 and usage['memorysize']>0.0 and usage['hdload']>0.0 and usage['hdsize']>0.0:
            if usage['cpuload']>0.0 and usage['hdsize']>0.0:
                cpuload.append(usage['cpuload'] / self.system.nodeFeatures[idx]['cpuload'])
##ReduceResourceElements                memorysize.append(usage['memorysize'] / self.system.nodeFeatures[idx]['memorysize'] )
##ReduceResourceElements                memoryload.append(usage['memoryload'] / self.system.nodeFeatures[idx]['memoryload'] )
                hdsize.append(usage['hdsize'] / self.system.nodeFeatures[idx]['hdsize'] )
##ReduceResourceElements                hdload.append(usage['hdload'] / self.system.nodeFeatures[idx]['hdload'] )

##ReduceResourceElements        return np.std(cpuload) + np.std(memorysize) + np.std(memoryload) + np.std(hdsize) + np.std(hdload)
        return np.std(cpuload) + np.std(hdsize)


#******************************************************************************************
#   END Cluster Balance use calculation
#******************************************************************************************





#******************************************************************************************
#   Failura calculation
#******************************************************************************************

    def calculateBlockFailure(self, blockDistribution):
        totalFailure = 1.0
        
        nodes = sorted(set(blockDistribution["rnode"]+blockDistribution["wnode"]))
        n=0
        while n<len(nodes):
            rack = nodes[n] / self.system.nodesXrack
            rackFailure = self.system.rackFeatures[rack]["failrate"]
            nodeFailure = 1.0
            while (n<len(nodes)) and (nodes[n] / self.system.nodesXrack == rack):
                nodeFailure = nodeFailure * self.system.nodeFeatures[nodes[n]]["failrate"]
                n+=1
            rackFailure = rackFailure + nodeFailure
            totalFailure = totalFailure * rackFailure
        
        return totalFailure

    def calculateFailure(self,solution):
        failure = 0.0
        for key in solution:
            failure = failure + self.calculateBlockFailure(solution[key])
        
        return failure


#    def calculateBlockFailure(self, blockDistribution):
#        totalFailure = 1.0
#        
#        nodes = sorted(set(blockDistribution["rnode"]+blockDistribution["wnode"]))
#        n=0
#        while n<len(nodes):
#            rack = nodes[n] / self.nodesXrack
#            rackFailure = self.rackFeatures[rack]["failrate"]
#            nodeFailure = 1.0
#            while (n<len(nodes)) and (nodes[n] / self.nodesXrack == rack):
#                nodeFailure *= self.nodeFeatures[nodes[n]]["failrate"]
#                n+=1
#            rackFailure = rackFailure + nodeFailure
#            totalFailure *= rackFailure
#        
#        return totalFailure
#
#    def calculateFailure(self,solution):
#        failure = 0.0
#        for key in solution:
#            failure += self.calculateBlockFailure(solution[key])
#        
#        return failure

#******************************************************************************************
#   END Failura calculation
#******************************************************************************************

#******************************************************************************************
#   NetworkLoad calculation
#******************************************************************************************

    def distanceBetweenNodes(self, a,b):
        
        rackA = a / self.system.nodesXrack
        rackB = b / self.system.nodesXrack
        distance = self.system.cpdNetwork[rackA][rackB]
        #print "from "+str(a)+" to "+str(b)+ " is "+str(distance)
                
        
        return distance

    def calculateBlockNetworkLoad(self, solution, block, inputFile, outputFile, MRjob):
        networkLoad = 0.0
        
        # calculation of the network distance and load for all the blocks of the tempfile for the readblocks of its MRjob and inputfile
        
        tempBlocksToUpdate = list(block['rnode']+block['wnode'])
        mapBlocks = []
        for key in solution:
            if key[0]==inputFile:
                mapBlocks.append(solution[key]['rnode'][self.system.MRjobsPerInputFile[inputFile].index(MRjob)])
        for n in tempBlocksToUpdate:
            for m in mapBlocks:
                networkLoad = networkLoad +  self.distanceBetweenNodes(n,m) * self.system.MRusage[MRjob]['probability'] * self.system.MRusage[MRjob]['networkload'] 
        

        tempBlockReadReduce = block['rnode']
        allOutputReplicas = []
        for key in solution:
            if key[0]==outputFile:
                allOutputReplicas += solution[key]['rnode'] + solution[key]['wnode']
        for n in tempBlockReadReduce:
            for m in allOutputReplicas:
                networkLoad = networkLoad +  self.distanceBetweenNodes(n,m) * self.system.MRusage[MRjob]['probability'] * self.system.MRusage[MRjob]['networkload'] 

        
        return networkLoad

    def calculateNetworkLoad(self,solution):
        networkLoad = 0.0
        for key in solution:
            if solution[key]['filetype']=='temp':
                tempfile = key[0]
                #busco cual es el job MR que corresponde a este fichero temporal
                #fileStructure = (i for i in self.system.MapReduceFiles if self.system.MapReduceFiles[i]['temp']==tempfile).next()
                #MRjob = fileStructure[0]          
                #inputfile = fileStructure[1]
                #outputfile = self.system.MapReduceFiles[fileStructure]['output']

                MRjob = self.system.MRjobsPerOutTempFile[tempfile]
                inputfile = self.system.FilesPerTempFiles[tempfile]['input']
                outputfile = self.system.FilesPerTempFiles[tempfile]['output']

                #print "The temp "+str(tempfile)+" is from input "+str(inputfile)+ " and generates "+str(outputfile)+ " for MRjob "+str(MRjob)
                networkLoad = networkLoad +  self.calculateBlockNetworkLoad(solution, solution[key], inputfile, outputfile, MRjob)
        
        return networkLoad
    
    def computeMagicStructure(self,structure):
        networkLoad = 0.0
        #inicio = time.time()
        for key in structure:
            replicas = structure[key]
            MRjob = replicas['mr']
            for i in replicas['readInput']:
                for j in replicas['writeTemp']:
                    networkLoad = networkLoad +  self.distanceBetweenNodes(i,j) * self.system.MRusage[MRjob]['probability'] * self.system.MRusage[MRjob]['networkload'] 
            for i in replicas['readTemp']:
                for j in replicas['writeOutput']:
                    networkLoad = networkLoad +  self.distanceBetweenNodes(i,j) * self.system.MRusage[MRjob]['probability'] * self.system.MRusage[MRjob]['networkload'] 
        #print "Tiempo de cálculo de sumar matriz:"+str(inicio - time.time())
        return networkLoad
        
        
    def magicCalculateNetworkLoad(self,solution):
        magicFilesStructure = copy.deepcopy(self.system.MagicFiles)
        #inicio = time.time()
        for key in solution:
            if solution[key]['filetype']=='input':
                inputId=key[0]
                for mrId in self.system.MRjobsPerInputFile[inputId]:
                    tempId=self.system.MapReduceFiles[(mrId,inputId)]['temp']
                    outputId=self.system.MapReduceFiles[(mrId,inputId)]['output']
                    magicFilesStructure[(inputId,tempId,outputId)]['readInput'] += solution[key]['rnode']
                #tengo que añadir los bloques en todos los que usan este inputID, por tanto he de buscar (*,inputId)
            elif solution[key]['filetype']=='temp':
                tempId=key[0]
                inputId = self.system.FilesPerTempFiles[tempId]['input']
                outputId = self.system.FilesPerTempFiles[tempId]['output']
                magicFilesStructure[(inputId,tempId,outputId)]['readTemp'] += solution[key]['rnode']
                magicFilesStructure[(inputId,tempId,outputId)]['writeTemp'] += solution[key]['rnode'] + solution[key]['wnode']

            elif solution[key]['filetype']=='output':
                outputId=key[0]
                inputId = self.system.FilesPerOutputFiles[outputId]['input']
                tempId = self.system.FilesPerOutputFiles[outputId]['temp']
                magicFilesStructure[(inputId,tempId,outputId)]['writeOutput'] += solution[key]['rnode'] + solution[key]['wnode']
        #print "Tiempo de generación matriz:"+str(inicio - time.time())
        
        return self.computeMagicStructure(magicFilesStructure)
#******************************************************************************************
#   END NetworkLoad calculation
#******************************************************************************************


#******************************************************************************************
#   Node Workload calculation
#******************************************************************************************

    def calculateNodesWorkload(self, chromosome):
        
        nodesLoad = []
        for i in range(self.system.nodenumber):
            #nodesLoad.append({"cpuload" : 0.0, "memorysize": 0.0, "memoryload": 0.0, "hdsize": 0.0, "hdload": 0.0})
            nodesLoad.append({"cpuload" : 0.0, "hdsize": 0.0})

        for key in chromosome:
            #añadir hdsize +1.0 por cada bloque
            #añadir hdloadwrite del MR con probabilidad de que este el MR en el sistema
            for element in (set(chromosome[key]['rnode']+chromosome[key]['wnode'])):
                nodesLoad[element]['hdsize']= nodesLoad[element]['hdsize'] + 1.0
                # añadir la carga sobre el hd al escribir
                if chromosome[key]['filetype']=='input':
                    #MRid = self.MRjobsPerInputFile[key[0]][chromosome[key]['rnode'].index(element)]
                    MRid = self.system.MRjobsPerInputFile[key[0]][0] #puede producirse que varios MRjobs ataquen al mismo archivo input. Pero solo hay un proceso que los escribe, por eso, cogemos solo la carga que genera uno de ellos sobre el archivo, y cogemos el que está en la posición 0
                else:
                    MRid = self.system.MRjobsPerOutTempFile[key[0]]
 ##ReduceResourceElements               nodesLoad[element]['hdload']= nodesLoad[element]['hdload'] + self.system.MRusage[MRid]['hdloadwrite'] * self.system.MRusage[MRid]['probability']  
                
                
                
            MRnodeIdPair = []  
            #obtenemos las parejas MR-nodeId de estos bloques
            if len(chromosome[key]['rnode'])>0:
                if (chromosome[key]['filetype']=='temp') or (chromosome[key]['filetype']=='output'):
                    #fileStructure = (i for i in self.MapReduceFiles if self.MapReduceFiles[i][chromosome[key]['filetype']]==key[0]).next()
                    #MRid = fileStructure[0]
                    MRid = self.system.MRjobsPerOutTempFile[key[0]]
                    nodeId = chromosome[key]['rnode'][0]
                    #print " el nodo "+ str(nodeId)+" tiene la carga del MR "+ str(MRid)
                    MRnodeIdPair.append((MRid,nodeId))
                if chromosome[key]['filetype']=='input':
                    for idx,rnod in enumerate(chromosome[key]['rnode']):
                        nodeId = rnod
                        MRid = self.system.MRjobsPerInputFile[key[0]][idx]
                        #print " el nodo "+ str(nodeId)+" tiene la carga del MR "+ str(MRid)
                        MRnodeIdPair.append((MRid,nodeId))
                        
            for MRNodeP in MRnodeIdPair:
                MRid = MRNodeP[0]
                nodeId = MRNodeP[1]
                #añadir hdloadread
  ##ReduceResourceElements              resourceComponent = 'hdloadread'
  ##ReduceResourceElements              nodesLoad[nodeId]['hdload']= nodesLoad[nodeId]['hdload'] + self.system.MRusage[MRid][resourceComponent] * self.system.MRusage[MRid]['probability']   
                #añadir memoryload
  ##ReduceResourceElements              resourceComponent = 'memoryload'
  ##ReduceResourceElements              nodesLoad[nodeId][resourceComponent]= nodesLoad[nodeId][resourceComponent] + self.system.MRusage[MRid][resourceComponent] * self.system.MRusage[MRid]['probability']  
                #añadir memorysize
 ##ReduceResourceElements               resourceComponent = 'memorysize'
 ##ReduceResourceElements               nodesLoad[nodeId][resourceComponent]= nodesLoad[nodeId][resourceComponent] + self.system.MRusage[MRid][resourceComponent] * self.system.MRusage[MRid]['probability']  
                #añadir cpuload
                resourceComponent = 'cpuload'
                nodesLoad[nodeId][resourceComponent]= nodesLoad[nodeId][resourceComponent] + self.system.MRusage[MRid][resourceComponent] * self.system.MRusage[MRid]['probability']  
                
        
        return nodesLoad
        
        
        
    def calculateSolutionsWorkload(self,pop):
        
        for i,citizen in enumerate(pop.population):
            pop.nodesUsages[i]=self.calculateNodesWorkload(citizen)
        

#******************************************************************************************
#   END Node Workload calculation
#******************************************************************************************



#******************************************************************************************
#   Model constraints
#******************************************************************************************

    def rackAwareness(self,chromosome):
        #check if at least two different racks are used     
        for key in chromosome:
            currentNodes = set(chromosome[key]['rnode'] + chromosome[key]['wnode'])
            currentNodes = {element / self.system.nodesXrack for element in currentNodes}
            if (len(currentNodes)<2):
                #print key
                #print currentNodes
                return False
        return True
    
    def nodea_lt_nodeb(self,a,b):
#ReduceResourceElements          for feature in ('cpuload','hdload','hdsize','memorysize','memoryload'):
        for feature in ('cpuload','hdsize'):
            if b[feature]<a[feature]:
                print "PEQUEÑÑÑÑÑÑÑÑOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
                return False
        return True
    
    def resourceUsages(self,nodes):
        for idx,v in enumerate(nodes):
            if not self.nodea_lt_nodeb(v,self.system.nodeFeatures[idx]):
                return False
        return True
    
    def checkConstraints(self,pop, index):
        
        chromosome = pop.population[index]
        if not self.rackAwareness(chromosome):
            #print chromosome
            return False
            
        nodesLoads = pop.nodesUsages[index]
        if not self.resourceUsages(nodesLoads):
            return False
        return True

#******************************************************************************************
#   END Model constraints
#******************************************************************************************


#******************************************************************************************
#   Objectives and fitness calculation
#******************************************************************************************


    def calculateFitnessObjectives(self, pop, index): #TODO
        #inicio = time.time()
        chr_fitness = {}
        chr_fitness["index"] = index
        #chr_fitness["performance"] = random.randint(1,100)
        
        chromosome=pop.population[index]
        nodeLoads= pop.nodesUsages[index]

        
        if self.checkConstraints(pop,index):
            chr_fitness["network"] = self.magicCalculateNetworkLoad(chromosome)
            #chr_fitness["network"] = 1.0
            chr_fitness["reliability"] = self.calculateFailure(chromosome)
            #chr_fitness["nodenumber"] = self.calculateNodeNumber(chromosome)
            if self.BalanceObjective:
                chr_fitness["balanceuse"] = self.calculateClusterBalanceUse(nodeLoads)
            #TODO redondear los valores de los fitness????
        else:
            chr_fitness["network"] = float('inf')
            chr_fitness["reliability"] = float('inf')
            #chr_fitness["nodenumber"] = float('inf')
            if self.BalanceObjective:
                chr_fitness["balanceuse"] = float('inf')
        #print "Tiempo de cálculo de todos los fitness:"+str(inicio - time.time())

            
        return chr_fitness
        
    def calculatePopulationFitnessObjectives(self,pop):   
        for index,citizen in enumerate(pop.population):
            cit_fitness = self.calculateFitnessObjectives(pop,index)
            pop.fitness[index] = cit_fitness
            
        print "[Fitness calculation]: Calculated **********************"       
        
         
    
#******************************************************************************************
#   END Objectives and fitness calculation
#******************************************************************************************




#******************************************************************************************
#   NSGA-II Algorithm
#******************************************************************************************

            
    def dominates(self,a,b):
        #checks if solution a dominates solution b, i.e. all the objectives are better in A than in B
        Adominates = True
        #### OJOOOOOO Hay un atributo en los dictionarios que no hay que tener en cuenta, el index!!!
        for key in a:
            if key!="index":  #por ese motivo está este if.
                if b[key]<=a[key]:
                    Adominates = False
                    break
        return Adominates        

        
    def crowdingDistancesAssigments(self,popT,front):
        
        for i in front:
            popT.crowdingDistances[i] = float(0)
            
        frontFitness = [popT.fitness[i] for i in front]
        #OJOOOOOO hay un atributo en el listado que es index, que no se tiene que tener en cuenta.
        for key in popT.fitness[0]:
            if key!="index":   #por ese motivo está este if.
                orderedList = sorted(frontFitness, key=lambda k: k[key])
                
                popT.crowdingDistances[orderedList[0]["index"]] = float('inf')
                minObj = orderedList[0][key]
                popT.crowdingDistances[orderedList[len(orderedList)-1]["index"]] = float('inf')
                maxObj = orderedList[len(orderedList)-1][key]
                
                normalizedDenominator = float(maxObj-minObj)
                if normalizedDenominator==0.0:
                    normalizedDenominator = float('inf')
        
                for i in range(1, len(orderedList)-1):
                    popT.crowdingDistances[orderedList[i]["index"]] += (orderedList[i+1][key] - orderedList[i-1][key])/normalizedDenominator

    def calculateCrowdingDistances(self,popT):
        
        i=0
        while len(popT.fronts[i])!=0:
            self.crowdingDistancesAssigments(popT,popT.fronts[i])
            i+=1


    def calculateDominants(self,popT):
        
        for i in range(len(popT.population)):
            popT.dominatedBy[i] = set()
            popT.dominatesTo[i] = set()
            popT.fronts[i] = set()

        for p in range(len(popT.population)):
            for q in range(p+1,len(popT.population)):
                if self.dominates(popT.fitness[p],popT.fitness[q]):
                    popT.dominatesTo[p].add(q)
                    popT.dominatedBy[q].add(p)
                if self.dominates(popT.fitness[q],popT.fitness[p]):
                    popT.dominatedBy[p].add(q)
                    popT.dominatesTo[q].add(p)        

    def calculateFronts(self,popT):

        addedToFronts = set()
        
        i=0
        while len(addedToFronts)<len(popT.population):
            popT.fronts[i] = set([index for index,item in enumerate(popT.dominatedBy) if item==set()])
            addedToFronts = addedToFronts | popT.fronts[i]
            
            for index,item in enumerate(popT.dominatedBy):
                if index in popT.fronts[i]:
                    popT.dominatedBy[index].add(-1)
                else:
                    popT.dominatedBy[index] = popT.dominatedBy[index] - popT.fronts[i]
            i+=1        
            
    def fastNonDominatedSort(self,popT):
        
        self.calculateDominants(popT)
        self.calculateFronts(popT)
             
    def plotFronts(self,popT,serieA,serieB):  
      
        f = 0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
        #while len(popT.fronts[f])!=0:
        while f<=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            #a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
            a = [thisfront[i][serieA] for i,v in enumerate(thisfront)]
            b = [thisfront[i][serieB] for i,v in enumerate(thisfront)]

            #ax1 = fig.add_subplot(111)
            
            ax.scatter(a, b, s=10, color=next(colors), marker="o")
            #ax1.annotate('a',(a,b))
            f +=1
        
        plt.show() 
        plt.close(fig)
        
        
    def plot3DFronts(self,popT):
        self.plot3DFronts0(popT)
        #self.plot3DFronts1(popT)
        #self.plot3DFronts2(popT)
        
    def plot3DFronts0(self,popT):  
          
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        f = 0

        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        #while len(popT.fronts[f])!=0:
        while f<=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["network"] for i,v in enumerate(thisfront)]
            c = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]


            ax.scatter(a, b, c, color=next(colors), marker="o")
            
            f +=1
    
        ax.set_xlabel('balanceuse')
        ax.set_ylabel('network')
        ax.set_zlabel('reliability')
    
        plt3d.show()  
        plt.close(fig)
        
        
    def plot3DFronts1(self,popT):  
          
        fig = plt.figure()
        #ax = fig.add_subplot(111, projection='3d')
        #ax = Axes3D(fig)
        ax = [fig.add_subplot(221, projection='3d'),
              fig.add_subplot(222),
              fig.add_subplot(223),
              fig.add_subplot(224)]
        f = 0

        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        #while len(popT.fronts[f])!=0:
        while f<=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["network"] for i,v in enumerate(thisfront)]
            c = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]


            ax[0].scatter(a, b, c, color=next(colors), marker="o")
            
            
            ax[1].plot(a, b, '+', markersize=.2, color='r')
            ax[2].plot(a, c, '+', markersize=.2, color='g')
            ax[3].plot(b, c, '+', markersize=.2, color='b') 
            
            
            f +=1
    
        ax[0].set_xlabel('balanceuse')
        ax[0].set_ylabel('network')
        ax[0].set_zlabel('reliability')
    
        plt3d.show() 
        plt.close(fig)

    def plot3DFronts2(self,popT):  
          
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #ax = Axes3D(fig)
        f = 0

        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        #while len(popT.fronts[f])!=0:
        while f<=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["network"] for i,v in enumerate(thisfront)]
            c = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]


            ax.scatter(a, b, c, color=next(colors), marker="o")
            
            ax.plot(a, b, '+', markersize=1., color='r', zdir='z', zs=0.0)
            ax.plot(a, c, '+', markersize=1., color='g', zdir='y', zs=0.0)
            ax.plot(b, c, '+', markersize=1., color='b', zdir='x', zs=0.0) 
            
            ax.set_xlim([0.0, 0.01])
            ax.set_ylim([0.0, 18.])
            ax.set_zlim([0.0, 0.004])
            
            
            f +=1
    
        ax.set_xlabel('balanceuse')
        ax.set_ylabel('network')
        ax.set_zlabel('reliability')
    
        plt3d.show() 
        plt.close(fig)
            
#******************************************************************************************
#   END NSGA-II Algorithm
#******************************************************************************************


#******************************************************************************************
#   Evolution based on NSGA-II 
#******************************************************************************************


    def generatePopulation(self,popT):
        for i in range(self.populationSize):
            chromosome = {}
        
            for fileId, numberOfBlocks in enumerate(self.system.blocksPerFile):
                try:
                    numberOfMRjobsForFile = len(self.system.MRjobsPerInputFile[fileId]) #when the file is a input file the number of MRjobs is considered
                    filetype = "input"
                except KeyError:
                    if fileId in self.system.tempFiles:
                        numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "temp"
                    elif fileId in self.system.outputFiles:
                        numberOfMRjobsForFile = 0 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "output"
                    else:
                        numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "ERROR"
#                except KeyError:
#                    numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
#                    filetype = "tempOutput"
                for blockId in range(numberOfBlocks):
                    if self.HadoopRulesCreation:
                        replicationFactor = 3
                    else:
                        replicationFactor = int(round(np.random.normal(3.0, 0.4))) # mean and standard deviation
                    
                    try:                   
                        if self.HadoopRulesCreation:
                            if replicationFactor-1>self.system.racknumber: #when the block replica is bigger than total node number, is set to the maximum
                                replicationFactor=self.system.racknumber                             
                            #metemos dos réplicas en un mismo armario y la tercera en otro
                            rackAllocation=random.sample(range(0, self.system.racknumber), replicationFactor-1)
                            allocation = []
                            for rack in rackAllocation:
                                shift = random.randint(0,self.system.nodesXrack-1)
                                allocation.append(rack*self.system.nodesXrack +shift)
                            shift2 = shift
                            while shift2 == shift:
                                shift = random.randint(0,self.system.nodesXrack-1)
                            allocation.append(rack*self.system.nodesXrack + shift)
                            
                        else:
                            if replicationFactor>self.system.nodenumber: #when the block replica is bigger than total node number, is set to the maximum
                                replicationFactor=self.system.nodenumber        
                            allocation=random.sample(range(0, self.system.nodenumber), replicationFactor) #random selection of the node to place the blocks
                            #selection of the nodes to be read by the tasks of the mapreduce job            
                    except ValueError:
                        print('Sample size exceeded population size.')
                    readallocation=[]
                    for x in range(numberOfMRjobsForFile): #chooising as many readnodes as MRjobs are associated  
                        readallocation.append(random.choice(allocation))
                    for readnode in iter(readallocation):
                        try:
                            allocation.remove(readnode)
                        except ValueError:
                            continue
                    chromosome[fileId,blockId] = {"filetype": filetype , "wnode":allocation,"rnode":readallocation}
            popT.population[i]=chromosome
            print "[Citizen generation]: Number %i generated**********************" % i
            #chr_fitness = self.calculateFitnessObjectives(chromosome,i)
            #popT.fitness[i]=chr_fitness
            #print "[Fitness calculation]: Calculated for citizen %i **********************" % i
            popT.dominatedBy[i]=set()
            popT.dominatesTo[i]=set()
            popT.fronts[i]=set()
            popT.crowdingDistances[i]=float(0)
            
        self.calculateSolutionsWorkload(popT)
        self.calculatePopulationFitnessObjectives(popT)
        self.fastNonDominatedSort(popT)
        if self.BalanceObjective:
            self.plot3DFronts(popT)
            self.plotFronts(popT,"balanceuse","network")
            self.plotFronts(popT,"balanceuse","reliability")

        self.plotFronts(popT,"network","reliability")
        self.calculateCrowdingDistances(popT)

    def tournamentSelection(self,k,popSize):
        selected = sys.maxint 
        for i in range(k):
            selected = min(selected,random.randint(0,popSize-1))
        return selected
           
    def fatherSelection(self, orderedFathers): #TODO
        i = self.tournamentSelection(2,len(orderedFathers))
        return  orderedFathers[i]["index"]
        
    def evolveToOffspring(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        orderedFathers = self.crowdedComparisonOrder(self.populationPt)
        

        #offspring generation

        while len(offspring.population)<self.populationSize:
            father1 = self.fatherSelection(orderedFathers)
            father2 = father1
            while father1 == father2:
                father2 = self.fatherSelection(orderedFathers)
###            print "[Father selection]: Father1: %i **********************" % father1
###            print "[Father selection]: Father1: %i **********************" % father2
            
            self.crossover(self.populationPt.population[father1],self.populationPt.population[father2],offspring.population)
        
        #offspring mutation
        
        for index,children in enumerate(offspring.population):
            if random.uniform(0,1) < self.mutationProbability:
                self.mutate(children)
###                print "[Offsrping generation]: Children %i MUTATED **********************" % index
            
        print "[Offsrping generation]: Population GENERATED **********************"  
        
        return offspring

        
    def crowdedComparisonOrder(self,popT):
        valuesToOrder=[]
        for i,v in enumerate(popT.crowdingDistances):
            citizen = {}
            citizen["index"] = i
            citizen["distance"] = v
            citizen["rank"] = 0
            valuesToOrder.append(citizen)
        
        f=0    
        while len(popT.fronts[f])!=0:
            for i,v in enumerate(popT.fronts[f]):
                valuesToOrder[v]["rank"]=f
            f+=1
             
        return sorted(valuesToOrder, key=lambda k: (k["rank"],-k["distance"]))

        
       
    def evolveNGSA2(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        offspring = self.evolveToOffspring()
        tiempo1 = time.time()
        tiempo2 = tiempo1
        print "Tiempo inicial:"+str(tiempo2-tiempo1)
        self.calculateSolutionsWorkload(offspring)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de calcular workload:"+str(tiempo2-tiempo1)
        timea = time.time()
        self.calculatePopulationFitnessObjectives(offspring)
        print "aaaaaa"+str(time.time()-timea)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de calcular fitness:"+str(tiempo2-tiempo1)
        
        timeb = time.time()
        populationRt = offspring.populationUnion(self.populationPt,offspring)
        print "bbbb"+str(time.time()-timeb)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de unir poblaciones:"+str(tiempo2-tiempo1)
        
        self.fastNonDominatedSort(populationRt)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de calcular NSGA2:"+str(tiempo2-tiempo1)
        
        self.calculateCrowdingDistances(populationRt)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de calcular crowding:"+str(tiempo2-tiempo1)

        
        orderedElements = self.crowdedComparisonOrder(populationRt)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de ordenar:"+str(tiempo2-tiempo1)
        
        finalPopulation = pop.POPULATION(self.populationSize)
        
        for i in range(self.populationSize):
            finalPopulation.population[i] = populationRt.population[orderedElements[i]["index"]]
            finalPopulation.fitness[i] = populationRt.fitness[orderedElements[i]["index"]]
            finalPopulation.nodesUsages[i] = populationRt.nodesUsages[orderedElements[i]["index"]]

        for i,v in enumerate(finalPopulation.fitness):
            finalPopulation.fitness[i]["index"]=i        
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo de copiar nueva generación:"+str(tiempo2-tiempo1)
        
        #self.populationPt = offspring
        self.populationPt = finalPopulation
        
        
        self.fastNonDominatedSort(self.populationPt)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo del segundo nsga2:"+str(tiempo2-tiempo1)

        self.calculateCrowdingDistances(self.populationPt)
        tiempo1,tiempo2 = tiempo2,time.time()
        print "Tiempo del segundo crowding distances:"+str(tiempo2-tiempo1)
        

        if self.BalanceObjective:
            self.plot3DFronts(self.populationPt)
            self.plotFronts(self.populationPt,"balanceuse","network")
            self.plotFronts(self.populationPt,"balanceuse","reliability")

        self.plotFronts(self.populationPt,"network","reliability")
        
        

 
        
       
        

#******************************************************************************************
#  END Evolution based on NSGA-II 
#******************************************************************************************





#blocksPerFilePerMapReduceJobs1 = np.array([[2,3,1],[5,5,0],[3,4,1],[8,3,1]])
#blocksPerFilePerMapReduceJobs = np.array([2,3,1])
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([5,5,0])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([3,4,1])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([8,3,1])))

#definition of the files for each MapReduce job. 1:1 jobs:files

#nodenumber = 50
#populationSize = 10
#population = []
#
#for i in range(populationSize):
#    chromosome = {}
#    fileId = 0
#    blockId = 0
#    
#    for (MRjobID,MRjobFileID), value in np.ndenumerate(blocksPerFilePerMapReduceJobs):
#        for blockId in range(value): #iteration of the three files of each mapreducejob
#            replicationFactor = int(round(np.random.normal(3.0, 0.4))) # mean and standard deviation
#            if replicationFactor>nodenumber: #when the block replica is bigger than total node number, is set to the maximum
#                replicationFactor=nodenumber        
#            try:
#                allocation=random.sample(range(1, nodenumber), replicationFactor) #random selection of the node to place the blocks
#                #selection of the nodes to be read by the tasks of the mapreduce job            
#                readallocation=[]
#                readnode = random.choice(allocation)
#                allocation.remove(readnode)
#                readallocation.append(readnode)
#            except ValueError:
#                print('Sample size exceeded population size.')
#            chromosome[fileId,blockId] = {"filetype": MRjobFileID % 3 , "wnode":allocation,"rnode":readallocation}
#            blockId+=1
#        fileId+=1
#    population.append(chromosome)
#    
#
#chromosome


#
#for fileId,totalBlock in enumerate(blocksPerFile):
#    for blockId in range(totalBlock):
#        chromosome[fileId,b] = {"wnode":[1,2,3],"rnode":[]}

