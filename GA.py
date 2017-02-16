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



class GA:
    
    
    
    def __init__(self):
        
        
        self.nodenumber = 50
        self.populationSize = 100
        self.population = []
        self.fitness = []
        self.dominatesTo = []
        self.dominatedBy = []
        self.fronts = []
        self.crowdingDistances = []
        self.mutationProbability = 0.10

        self.MapReduceFiles = {}
        MRJobId=0
        fileId=0
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 1 ,"output": 2}
        fileId=3
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 4 ,"output": 5}
        MRJobId=1
        fileId=0
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 6 ,"output": 7}
        
        self.blocksPerFile = []
        self.blocksPerFile = [4,2,1,5,4,0,1,1]
        
        self.tempFiles = set()
        self.outputFiles = set()
        
        self.MRjobsPerInputFile = {} #a dictionary indexed by file id with the mapreduces that access to that fileid
        self.InputFilesPerMRJob = {} # indexed by mr id with the files that this MR accesses
        
        for mrKey,fileKey in self.MapReduceFiles:
            try:
                self.MRjobsPerInputFile[fileKey].append(mrKey)
            except KeyError:
                self.MRjobsPerInputFile[fileKey] = [mrKey]
            try:
                self.InputFilesPerMRJob[mrKey].append(fileKey)
            except KeyError:
                self.InputFilesPerMRJob[mrKey] = [fileKey]
            self.tempFiles.add(self.MapReduceFiles[(mrKey,fileKey)]['temp'])
            self.outputFiles.add(self.MapReduceFiles[(mrKey,fileKey)]['output'])
            
        

#******************************************************************************************
#   MUTATIONS
#******************************************************************************************

    def swapTwoSchedulleMutation(self,blockDef): #swap the nodes where the MRjobs are schedulled for two MRjobs
#        print blockDef
        swapIdx = random.sample(range(0,len(blockDef['rnode'])),2)
        blockDef['rnode'][swapIdx[0]], blockDef['rnode'][swapIdx[1]] =  blockDef['rnode'][swapIdx[1]], blockDef['rnode'][swapIdx[0]]
#        print blockDef    
        print "[Offsrping generation]: Swap Two Schedulled Mutation **********************"
        
    def swapBlockSchedulleMutation(self,blockDef): #swap the nodes where a MRjobs is schedulled with the node in which other copy of the block is stored
#        print blockDef
        schIdx = random.randint(0,len(blockDef['rnode'])-1)
        blckIdx = random.randint(0,len(blockDef['wnode'])-1)
        blockDef['rnode'][schIdx], blockDef['wnode'][blckIdx] =  blockDef['wnode'][blckIdx], blockDef['rnode'][schIdx]
#        print blockDef    
        print "[Offsrping generation]: Swap Schedulle and Block Mutation **********************"
        
    def changeSchedulleMutation(self,blockDef): #alter the value of the nodes where a MRjob is schedulled
#        print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.nodenumber: 
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.nodenumber-1)
            schIdx = random.randint(0,len(blockDef['rnode'])-1)
            blockDef['rnode'][schIdx]=newNode
 #           print blockDef    
            print "[Offsrping generation]: Change Schedulle Node Mutation **********************"
        else:
            print "[Offsrping generation]: Change Schedulle Node Mutation ERROR the block is stored in all the nodes **********************"
        
        
    def changeBlockMutation(self,blockDef): #alter the value of the nodes where a block is stored
#        print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.nodenumber: 
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.nodenumber-1)
            blckIdx = random.randint(0,len(blockDef['wnode'])-1)
            blockDef['wnode'][blckIdx]=newNode
#            print blockDef    
            print "[Offsrping generation]: Change Block Node Mutation **********************"
        else:
            print "[Offsrping generation]: Change Block Node Mutation ERROR the block is stored in all the nodes **********************"
    
    
    def addBlockMutation(self,blockDef): #add a new node to store a replica of the block
 #       print blockDef
        inUse = set(blockDef['rnode']+blockDef['wnode'])
        if len(inUse)<self.nodenumber:
            newNode= None
            while newNode in inUse or newNode is None:
                newNode = random.randint(0,self.nodenumber-1)
            blockDef['wnode'].append(newNode)
#            print blockDef    
            print "[Offsrping generation]: Add Block Mutation **********************"
        else:
            print "[Offsrping generation]: Add Block Mutation ERROR the block is stored in all the nodes **********************"
        
        
    def delBlockMutation(self,blockDef): #remove a node where a block replica is stored
#        print blockDef
        blckIdx = random.randint(0,len(blockDef['wnode'])-1)
        blockDef['wnode'].pop(blckIdx)
#        print blockDef    
        print "[Offsrping generation]: Del Block Mutation **********************"
        
    
    
    
    def mutate(self,child):
        blockSelected = random.randint(0,len(child)-1)
        blockSelectedKey = child.keys()[blockSelected]
        print "[Offsrping generation]: Mutation of block %s in process**********************" % str(blockSelectedKey)
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
        print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        print "[Offsrping generation]: Children 2 added **********************"



#******************************************************************************************
#   END CROSSOVER
#******************************************************************************************




    def generatePopulation(self):
        for i in range(self.populationSize):
            chromosome = {}
        
            for fileId, numberOfBlocks in enumerate(self.blocksPerFile):
                try:
                    numberOfMRjobsForFile = len(self.MRjobsPerInputFile[fileId]) #when the file is a input file the number of MRjobs is considered
                    filetype = "input"
                except KeyError:
                    if fileId in self.tempFiles:
                        numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "temp"
                    elif fileId in self.outputFiles:
                        numberOfMRjobsForFile = 0 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "output"
                    else:
                        numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
                        filetype = "ERROR"
#                except KeyError:
#                    numberOfMRjobsForFile = 1 #if not, the number of MRfiles that access this file is 1 because is a temp or output file
#                    filetype = "tempOutput"
                for blockId in range(numberOfBlocks):
                    replicationFactor = int(round(np.random.normal(3.0, 0.4))) # mean and standard deviation
                    if replicationFactor>self.nodenumber: #when the block replica is bigger than total node number, is set to the maximum
                        replicationFactor=self.nodenumber        
                    try:
                        allocation=random.sample(range(1, self.nodenumber), replicationFactor) #random selection of the node to place the blocks
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
            self.population.append(chromosome)
            print "[Citizen generation]: Number %i generated**********************" % i
            chr_fitness = self.calculateFitness(chromosome,i)
            self.fitness.append(chr_fitness)
            print "[Fitness calculation]: Calculated for citizen %i **********************" % i
            self.dominatedBy.append(set())
            self.dominatesTo.append(set())
            self.fronts.append(set())
            self.crowdingDistances.append(float(0))
            
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


    def calculateFitness(self, chromosome, index): #TODO
        chr_fitness = {}
        chr_fitness["index"] = index
        chr_fitness["performance"] = random.randint(1,100)
        #chr_fitness["network"] = random.randint(1,100)
        chr_fitness["reliability"] = random.randint(1,100)
        return chr_fitness
    
        
    def crowdignDistancesAssigments(self,front):
        
        for i in front:
            self.crowdingDistances[i] = float(0)
            
        frontFitness = [self.fitness[i] for i in front]
        #OJOOOOOO hay un atributo en el listado que es index, que no se tiene que tener en cuenta.
        for key in self.fitness[0]:
            if key!="index":   #por ese motivo está este if.
                orderedList = sorted(frontFitness, key=lambda k: k[key])
                
                self.crowdingDistances[orderedList[0]["index"]] = float('inf')
                minObj = orderedList[0][key]
                self.crowdingDistances[orderedList[len(orderedList)-1]["index"]] = float('inf')
                maxObj = orderedList[len(orderedList)-1][key]
                
                normalizedDenominator = float(maxObj-minObj)
        
                for i in range(1, len(orderedList)-1):
                    self.crowdingDistances[orderedList[i]["index"]] += (orderedList[i+1][key] - orderedList[i-1][key])/normalizedDenominator

     


    def calculateDominants(self):
        
        for i in range(self.populationSize):
            self.dominatedBy[i] = set()
            self.dominatesTo[i] = set()
            self.fronts[i] = set()

        for p in range(self.populationSize):
            for q in range(p+1,self.populationSize):
                if self.dominates(self.fitness[p],self.fitness[q]):
                    self.dominatesTo[p].add(q)
                    self.dominatedBy[q].add(p)
                if self.dominates(self.fitness[q],self.fitness[p]):
                    self.dominatedBy[p].add(q)
                    self.dominatesTo[q].add(p)        

    def calculateFronts(self):

        addedToFronts = set()
        
        i=0
        while len(addedToFronts)<self.populationSize:
            self.fronts[i] = set([index for index,item in enumerate(self.dominatedBy) if item==set()])
            addedToFronts = addedToFronts | self.fronts[i]
            
            for index,item in enumerate(self.dominatedBy):
                if index in self.fronts[i]:
                    self.dominatedBy[index].add(-1)
                else:
                    self.dominatedBy[index] = self.dominatedBy[index] - self.fronts[i]
            i+=1        
            
    def fastNonDominatedSort(self):
        
        self.calculateDominants()
        self.calculateFronts()
             
    def plotFronts(self):  
      
        f = 0
        #fig = plt.figure()
        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
        while len(self.fronts[f])!=0:
            thisfront = [self.fitness[i] for i in self.fronts[f]]

            a = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["performance"] for i,v in enumerate(thisfront)]

            #ax1 = fig.add_subplot(111)
            
            plt.scatter(a, b, s=10, color=next(colors), marker="o")
            #ax1.annotate('a',(a,b))
            f +=1
        
        plt.show()        
    def fatherSelection(self): #TODO
        return random.randint(0,self.populationSize-1)    
        
    def evolve(self):
        
        offspring = []
        

        #offspring generation

        while len(offspring)<self.populationSize:
            father1 = self.fatherSelection()
            father2 = father1
            while father1 == father2:
                father2 = self.fatherSelection()
            print "[Father selection]: Father1: %i **********************" % father1
            print "[Father selection]: Father1: %i **********************" % father2
            self.crossover(self.population[father1],self.population[father2],offspring)
        
        #offspring mutation
        
        for index,children in enumerate(offspring):
            if random.uniform(0,1) < self.mutationProbability:
                self.mutate(children)
                print "[Offsrping generation]: Children %i MUTATED **********************" % index
            
        print "[Offsrping generation]: Population GENERATED **********************"  
        self.population = offspring
        offspringfitness = []
        for index,citizen in iter(self.population):
            cit_fitness = self.calculateFitness(citizen,index)
            offspringfitness.append(cit_fitness)
        self.fitness = offspringfitness
            
        print "[Fitness calculation]: Calculated **********************"
        
        






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

