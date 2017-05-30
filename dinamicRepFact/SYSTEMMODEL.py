#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""
import copy
import random as random
import math as math


class SYSTEMMODEL:
    
    def __init__(self):
        
        self.nodenumber = 0
        self.racknumber = 0 #el nodenumber ha de ser divisible por este numero
        self.nodesXrack = 0
        
        self.migrationBetweenRacks = 10
        self.migrationBetweenNodes = 1
        
        self.rnd = random.Random()
        self.rnd.seed(100)
        
        self.initialAllocation = {}
        
#    def normalizeConfiguration(self):
#        for i,v in enumerate(self.serviceTupla):
#            self.serviceTupla[i]['scaleLevel']= int(math.ceil((self.serviceTupla[i]['computationalResources']*self.serviceTupla[i]['requestNumber']*self.requestPerApp[self.serviceTupla[i]['application']])/self.serviceTupla[i]['threshold']))
#            self.serviceTupla[i]['containerUsage']= self.serviceTupla[i]['computationalResources']/self.serviceTupla[i]['scaleLevel'] 




#################
#
#
#
#
#    CONFIGURACION A
#
#
#
#
################
        
    def configurationA(self,nodes):

        self.nodenumber = nodes
        self.racknumber = 5 #el nodenumber ha de ser divisible por este numero
        self.nodesXrack = self.nodenumber / self.racknumber
        

#******************************************************************************************
#   Definición de la red del CPD
#******************************************************************************************



        self.cpdNetwork = [[0 for x in range(self.racknumber)] for y in range(self.racknumber)]
        
        for r in range(self.racknumber):
            for s in range(self.racknumber):
                self.cpdNetwork[r][s]=12.0
                self.cpdNetwork[s][r]=12.0
            self.cpdNetwork[r][r]=5.0                  
                            

#******************************************************************************************
#   END Definición de la red del CPD
#******************************************************************************************

  
#******************************************************************************************
#   Definición de los recursos de los nodos, y de la distribución de los nodos en armarios
#******************************************************************************************

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
        self.plantillasMaquinas.append({"name": "tinny", "cpuload" : 1.0, "memorysize": 4.0, "memoryload": 1.0, "hdsize": 12.0, "hdload": 1.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "small", "cpuload" : 2.0, "memorysize": 8.0, "memoryload": 1.0, "hdsize": 12.0, "hdload": 1.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "big", "cpuload" : 8.0, "memorysize": 32.0, "memoryload": 1.0, "hdsize": 12.0, "hdload": 1.0, "failrate": 0.01})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])
        

        self.rackFeatures = []
        for r in range (self.racknumber):
            self.rackFeatures.append({"failrate": 0.03}) 
            
        #distribuimos los nodos en los armarios de forma uniforme

        #consideraremos que las máquinas están distribuidas secuencialmente sobre los racks, es decir, el primer rack tiene
        #desde la máquina 0 hasta la nodeXrack - 1, en el segundo desde la nodeXrack hasta la 2*nodeXrack - 1... y asi...
        
#        self.rackNodes = []
#        nonAssignedNodes = set(range(self.nodenumber))
#        for r in range(self.racknumber):
#            self.rackNodes.append(set(random.sample(nonAssignedNodes, min(self.nodenumber / self.racknumber, len(nonAssignedNodes)))))
#            nonAssignedNodes -= self.rackNodes[r]
#        for r in range(self.racknumber):
#            if len(nonAssignedNodes)!=0:
#                self.rackNodes[r] |= set(random.sample(nonAssignedNodes, 1))
#                nonAssignedNodes -= self.rackNodes[r]
        

#******************************************************************************************
#   END Definición de los recursos de los nodos
#******************************************************************************************
      
        
        
#******************************************************************************************
#   Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************

        
        #Para cada uno de los jobs MR que tengamos MRJobId, hemos de indicar el fichero sobre el que se van a ejecutar fileId. Y para cada
        #fichero sobre el que un MR se ejecute , debemos de indicar el identificador del fichero en el que se escribirn
        #los resultados parciales del task map "temp" y los resultados finales del task reduce "output"
        self.MagicFiles = {}
        
        self.MapReduceFiles = {}
        MRJobId=0
        fileId=0
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 1 ,"output": 2}
        self.MagicFiles[0,1,2]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":0 }
            
        fileId=3
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 4 ,"output": 5}
        self.MagicFiles[3,4,5]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":0  }
        
        MRJobId=1
        fileId=0
        self.MapReduceFiles[MRJobId,fileId] = {"temp": 6 ,"output": 7}
        self.MagicFiles[0,6,7]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":1 }
        



        ####
        # probability es la probabilidad de que este proceso se encuentre en el sistema, o el %/100 del tiempo que está usando recursos
        # networkload es la carga que se genera sobre la red cuando un proceso map ejecutado sobre un bloque de lectura rnode tiene que escribir su resultado en un UNICO bloque del fichero temporal que genera
        #             de la misma forma que es igual a la carga que genera un proceso reduce ejecutadosobre un bloque rnode y tiene que escribir el output en un UNICO bloque del fichero output final que genera

        self.MRusage= []
        MRJobId=0
        self.MRusage.append({"cpuload" : 0.01, "memorysize": 0.2, "memoryload": 0.04, "hdloadread": 0.08, "hdloadwrite": 0.08, "networkload": 1.0, "probability": 0.01})
        MRJobId=1
        self.MRusage.append({"cpuload" : 0.01, "memorysize": 0.2, "memoryload": 0.04, "hdloadread": 0.08, "hdloadwrite": 0.08, "networkload": 1.0, "probability": 0.01})
        

        #Para cada fichero que hemos definido anteriormente \all fileid + \all temp + \all output, hemos de indicar el tamaño
        # de cada uno de ellos self.blocksPerFile. El tamaño viene dado por el número de bloques que ocupará. Y el índice del list corresponde al id del fichero
        self.blocksPerFile = []
        self.blocksPerFile = [4,2,1,5,4,0,1,1]
        
#******************************************************************************************
#   END Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************


        #Las variables siguientes no las tiene que definir el suario, las creamos para facilitar los cálculos, pero se crean a partir de las variables anteriormente definidas


        self.FilesPerTempFiles = {}
        self.FilesPerOutputFiles = {}


        for key in self.MapReduceFiles:
            fitem = self.MapReduceFiles[key]
            self.FilesPerTempFiles[fitem['temp']] = {"input" : key[1], "output": fitem['output']}
            self.FilesPerOutputFiles[fitem['output']] = {"input" : key[1], "temp": fitem['temp']}



        self.tempFiles = set()
        self.outputFiles = set()
        
        self.MRjobsPerInputFile = {} #a dictionary indexed by file id with the mapreduces that access to that fileid
        self.InputFilesPerMRJob = {} # indexed by mr id with the files that this MR accesses
        self.MRjobsPerOutTempFile = {}
        
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
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['temp']] = mrKey
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['output']] = mrKey
                                                          
        

#################
#
#
#
#
#    CONFIGURACION B
#
#
#
#
################
        
    def configurationB(self,nodes):
        
        nodenumber=100
        racknumber=10
        num_mr=25
        num_files=50
        inputFileSize = 100
        tempFileSize = 100
        outputFileSize = 100
        tantoAdicional = 0.15
        
        
        

        self.nodenumber = nodenumber
        self.racknumber = racknumber #el nodenumber ha de ser divisible por este numero
        self.nodesXrack = self.nodenumber / self.racknumber
        

#******************************************************************************************
#   Definición de la red del CPD
#******************************************************************************************



        self.cpdNetwork = [[0 for x in range(self.racknumber)] for y in range(self.racknumber)]
        
        for r in range(self.racknumber):
            for s in range(self.racknumber):
                self.cpdNetwork[r][s]=12.0
                self.cpdNetwork[s][r]=12.0
            self.cpdNetwork[r][r]=5.0                  
                            

#******************************************************************************************
#   END Definición de la red del CPD
#******************************************************************************************

  
#******************************************************************************************
#   Definición de los recursos de los nodos, y de la distribución de los nodos en armarios
#******************************************************************************************

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "tinny", "cpuload" : 1.0, "memorysize": 4.0, "memoryload": 1.0, "hdsize": 1600.0, "hdload": 1.0, "failrate": 0.001})
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "small", "cpuload" : 2.0, "memorysize": 8.0, "memoryload": 1.0, "hdsize": 4000.0, "hdload": 1.0, "failrate": 0.005})
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "big", "cpuload" : 8.0, "memorysize": 32.0, "memoryload": 1.0, "hdsize": 8000.0, "hdload": 1.0, "failrate": 0.015})
        self.plantillasMaquinas.append({"name": "tinny", "cpuload" : 1.0, "hdsize": 1600.0, "failrate": 0.001})
        self.plantillasMaquinas.append({"name": "small", "cpuload" : 2.0, "hdsize": 4000.0, "failrate": 0.005})
        self.plantillasMaquinas.append({"name": "big", "cpuload" : 8.0, "hdsize": 8000.0, "failrate": 0.015})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        self.nodeFeatures = []
    
        #Los 5 primeros racks tienen máquinas del tipo tinny
        for n in range(0,50):
            self.nodeFeatures.append(self.plantillasMaquinas[0])
        #Los siguientes 5  racks tienen máquinas del tipo small
        for n in range(50,100):
            self.nodeFeatures.append(self.plantillasMaquinas[1])            
            
        #Los siguientes 5  racks tienen máquinas del tipo big
        for n in range(100,150):
            self.nodeFeatures.append(self.plantillasMaquinas[2])    
        #Los últimos 5 racks tienen máquinas mezcladas.
        tipomaquina=0
        for n in range(150,200):
            self.nodeFeatures.append(self.plantillasMaquinas[tipomaquina])
            tipomaquina = (tipomaquina+1)%3

        self.rackFeatures = []
        for r in range (self.racknumber):
            self.rackFeatures.append({"failrate": 0.03}) 
            
        #distribuimos los nodos en los armarios de forma uniforme

        #consideraremos que las máquinas están distribuidas secuencialmente sobre los racks, es decir, el primer rack tiene
        #desde la máquina 0 hasta la nodeXrack - 1, en el segundo desde la nodeXrack hasta la 2*nodeXrack - 1... y asi...
        
#      

#******************************************************************************************
#   END Definición de los recursos de los nodos
#******************************************************************************************
      
        
        
#******************************************************************************************
#   Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************



        ####
        # probability es la probabilidad de que este proceso se encuentre en el sistema, o el %/100 del tiempo que está usando recursos
        # networkload es la carga que se genera sobre la red cuando un proceso map ejecutado sobre un bloque de lectura rnode tiene que escribir su resultado en un UNICO bloque del fichero temporal que genera
        #             de la misma forma que es igual a la carga que genera un proceso reduce ejecutadosobre un bloque rnode y tiene que escribir el output en un UNICO bloque del fichero output final que genera

        
        
        self.MRusage= []        
        
        for mri in range(num_mr):

            MRJobId=mri
            cpu = self.rnd.random()/10
            prob = self.rnd.random()/num_mr
#ReduceResourceElements            self.MRusage.append({"cpuload" : cpu, "memorysize": 0.0, "memoryload": 0.0, "hdloadread": 0.0, "hdloadwrite": 0.0, "networkload": 1.0, "probability": prob})
            self.MRusage.append({"cpuload" : cpu, "networkload": 1.0, "probability": prob})
        



        
        #Para cada uno de los jobs MR que tengamos MRJobId, hemos de indicar el fichero sobre el que se van a ejecutar fileId. Y para cada
        #fichero sobre el que un MR se ejecute , debemos de indicar el identificador del fichero en el que se escribirn
        #los resultados parciales del task map "temp" y los resultados finales del task reduce "output"
        
        
        
        self.MapReduceFiles = {}
        self.blocksPerFile = []
        self.MagicFiles = {}
        
        
        #asigno al menos un map reduce a cada fichero
        for fi in range(num_files):
            MRJobId=self.rnd.randint(0,len(self.MRusage)-1)
            fileId=fi*3
            inputSize = self.rnd.randint(1,inputFileSize)
            tmpSize = self.rnd.randint(1,tempFileSize)
            outputSize = self.rnd.randint(1,outputFileSize)
            self.MapReduceFiles[MRJobId,fileId] = {"temp": fileId+1 ,"output": fileId+2}
            self.MagicFiles[fileId,fileId+1,fileId+2]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":MRJobId }
            self.blocksPerFile.append(inputSize)
            self.blocksPerFile.append(tmpSize)
            self.blocksPerFile.append(outputSize)

        #añado un % tantoadicional de relaciones mr-file adicionales de forma totalmente aleatorio
        
        currentFileId = 3 * num_files
        moreRelationships = int(math.ceil(num_files * tantoAdicional))
        for fi in range(moreRelationships):
            fileId=self.rnd.randint(0,num_files-1)*3
            MRJobId=self.rnd.randint(0,len(self.MRusage)-1)
            while (MRJobId,fileId) in self.MapReduceFiles:
                MRJobId=self.rnd.randint(0,len(self.MRusage)-1)
            self.MapReduceFiles[MRJobId,fileId] = {"temp": currentFileId ,"output": currentFileId+1}  
            self.MagicFiles[fileId,currentFileId,currentFileId+1]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":MRJobId }
            tmpSize = self.rnd.randint(1,200)
            outputSize = self.rnd.randint(1,200)
            self.blocksPerFile.append(tmpSize)
            self.blocksPerFile.append(outputSize)
            currentFileId = currentFileId + 2      



            
            
        #Para cada fichero que hemos definido anteriormente \all fileid + \all temp + \all output, hemos de indicar el tamaño
        # de cada uno de ellos self.blocksPerFile. El tamaño viene dado por el número de bloques que ocupará. Y el índice del list corresponde al id del fichero

        
#******************************************************************************************
#   END Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************


        #Las variables siguientes no las tiene que definir el suario, las creamos para facilitar los cálculos, pero se crean a partir de las variables anteriormente definidas


        self.FilesPerTempFiles = {}
        self.FilesPerOutputFiles = {}


        for key in self.MapReduceFiles:
            fitem = self.MapReduceFiles[key]
            self.FilesPerTempFiles[fitem['temp']] = {"input" : key[1], "output": fitem['output']}
            self.FilesPerOutputFiles[fitem['output']] = {"input" : key[1], "temp": fitem['temp']}



        self.tempFiles = set()
        self.outputFiles = set()
        
        self.MRjobsPerInputFile = {} #a dictionary indexed by file id with the mapreduces that access to that fileid
        self.InputFilesPerMRJob = {} # indexed by mr id with the files that this MR accesses
        self.MRjobsPerOutTempFile = {}
        
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
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['temp']] = mrKey
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['output']] = mrKey
 
                                                          
                                                          
                                                          
                                                          
#################
#
#
#
#
#    CONFIGURACION MORM
#
#
#
#
################
        
    def configurationMORM(self,nodes):
        
        nodenumber=8
        racknumber=4
        
        
        blockSize = 64


        self.nodenumber = nodenumber
        self.racknumber = racknumber #el nodenumber ha de ser divisible por este numero
        self.nodesXrack = self.nodenumber / self.racknumber
        
        #tamaños de los ficheros en megas
        self.inputFileSizes = [1600, 1623, 1646, 1671, 1696, 1723, 1750, 1779, 1809, 1839, 1872, 1905, 1941, 1977, 2016, 2056, 2099, 2143, 2190, 2239, 2292, 2347, 2406, 2468, 2535, 2606, 2681, 2763, 2851, 2946, 3049, 3161, 3283, 3418, 3567, 3733, 3918, 4128, 4367, 4643, 4965, 5347, 5810, 6382, 7113, 8087, 9462, 11586, 15412, 25101]
        self.tempFileSizes = [1600, 1623, 1646, 1671, 1696, 1723, 1750, 1779, 1809, 1839, 1872, 1905, 1941, 1977, 2016, 2056, 2099, 2143, 2190, 2239, 2292, 2347, 2406, 2468, 2535, 2606, 2681, 2763, 2851, 2946, 3049, 3161, 3283, 3418, 3567, 3733, 3918, 4128, 4367, 4643, 4965, 5347, 5810, 6382, 7113, 8087, 9462, 11586, 15412, 25101]
        self.outputFileSizes = [1600, 1623, 1646, 1671, 1696, 1723, 1750, 1779, 1809, 1839, 1872, 1905, 1941, 1977, 2016, 2056, 2099, 2143, 2190, 2239, 2292, 2347, 2406, 2468, 2535, 2606, 2681, 2763, 2851, 2946, 3049, 3161, 3283, 3418, 3567, 3733, 3918, 4128, 4367, 4643, 4965, 5347, 5810, 6382, 7113, 8087, 9462, 11586, 15412, 25101]

        num_files=len(self.inputFileSizes)
        num_mr=num_files
        
        #transformamos el tamaño de los ficheros a bloques
        for i in range(num_files):
            self.inputFileSizes[i]=self.inputFileSizes[i]/blockSize
        for i in range(num_files):
            self.tempFileSizes[i]=int(0.10*self.tempFileSizes[i]/blockSize)
        for i in range(num_files):
            self.outputFileSizes[i]=int(0.05*self.outputFileSizes[i]/blockSize)


        self.fileAccess =[125 ,77 ,57 ,47 ,40 ,35 ,31 ,29 ,26 ,24 ,23 ,21 ,20 ,19 ,18 ,17 ,17 ,16 ,15 ,15, 14 ,14 ,13 ,13 ,13 ,12 ,12 ,12 ,11 ,11, 11 ,10 ,10 ,10 ,10 ,10 ,9 ,9 ,9 ,9, 9 ,9 ,8 ,8 ,8 ,8 ,8 ,8 ,8 ,7]        
        self.totalFileAccesses = sum(self.fileAccess)
#******************************************************************************************
#   Definición de la red del CPD
#******************************************************************************************



        self.cpdNetwork = [[0 for x in range(self.racknumber)] for y in range(self.racknumber)]
        
        for r in range(self.racknumber):
            for s in range(self.racknumber):
                self.cpdNetwork[r][s]=12.0
                self.cpdNetwork[s][r]=12.0
            self.cpdNetwork[r][r]=5.0                  
                            

#******************************************************************************************
#   END Definición de la red del CPD
#******************************************************************************************

  
#******************************************************************************************
#   Definición de los recursos de los nodos, y de la distribución de los nodos en armarios
#******************************************************************************************

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "tinny", "cpuload" : 1.0, "memorysize": 4.0, "memoryload": 1.0, "hdsize": 1600.0, "hdload": 1.0, "failrate": 0.001})
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "small", "cpuload" : 2.0, "memorysize": 8.0, "memoryload": 1.0, "hdsize": 4000.0, "hdload": 1.0, "failrate": 0.005})
#ReduceResourceElements        self.plantillasMaquinas.append({"name": "big", "cpuload" : 8.0, "memorysize": 32.0, "memoryload": 1.0, "hdsize": 8000.0, "hdload": 1.0, "failrate": 0.015})


#        self.plantillasMaquinas.append({"name": "tinny", "cpuload" : 1.0, "hdsize": 1600.0, "failrate": 0.001})
#        self.plantillasMaquinas.append({"name": "small", "cpuload" : 2.0, "hdsize": 4000.0, "failrate": 0.005})
#        self.plantillasMaquinas.append({"name": "big", "cpuload" : 8.0, "hdsize": 8000.0, "failrate": 0.015})

        self.plantillasMaquinas.append({"name": "p1", "cpuload" : 1.0, "hdsize": 500.0, "failrate": 0.001})
        self.plantillasMaquinas.append({"name": "p2", "cpuload" : 2.0, "hdsize": 500.0, "failrate": 0.005})
        self.plantillasMaquinas.append({"name": "p3", "cpuload" : 8.0, "hdsize": 100.0, "failrate": 0.001})
        self.plantillasMaquinas.append({"name": "p4", "cpuload" : 8.0, "hdsize": 240.0, "failrate": 0.002})
        self.plantillasMaquinas.append({"name": "p5", "cpuload" : 8.0, "hdsize": 250.0, "failrate": 0.015})
        self.plantillasMaquinas.append({"name": "p6", "cpuload" : 8.0, "hdsize": 160.0, "failrate": 0.012})
        self.plantillasMaquinas.append({"name": "p7", "cpuload" : 8.0, "hdsize": 128.0, "failrate": 0.004})
        self.plantillasMaquinas.append({"name": "p8", "cpuload" : 8.0, "hdsize": 146.0, "failrate": 0.007})

        #transformamos el tamaño del HD de las plantillas que está indicado en GB a bloques
        for i in range(len(self.plantillasMaquinas)):
            self.plantillasMaquinas[i]['hdsize']=self.plantillasMaquinas[i]['hdsize']*1024/blockSize
        
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        self.nodeFeatures = []

        for n in range(0,8):
            self.nodeFeatures.append(self.plantillasMaquinas[n])
    

        self.rackFeatures = []
        for r in range (self.racknumber):
            self.rackFeatures.append({"failrate": 0.03}) 
            
        #distribuimos los nodos en los armarios de forma uniforme

        #consideraremos que las máquinas están distribuidas secuencialmente sobre los racks, es decir, el primer rack tiene
        #desde la máquina 0 hasta la nodeXrack - 1, en el segundo desde la nodeXrack hasta la 2*nodeXrack - 1... y asi...
        
#      

#******************************************************************************************
#   END Definición de los recursos de los nodos
#******************************************************************************************
      
        
        
#******************************************************************************************
#   Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************



        ####
        # probability es la probabilidad de que este proceso se encuentre en el sistema, o el %/100 del tiempo que está usando recursos
        # networkload es la carga que se genera sobre la red cuando un proceso map ejecutado sobre un bloque de lectura rnode tiene que escribir su resultado en un UNICO bloque del fichero temporal que genera
        #             de la misma forma que es igual a la carga que genera un proceso reduce ejecutadosobre un bloque rnode y tiene que escribir el output en un UNICO bloque del fichero output final que genera

        
        
        self.MRusage= []        
        
        for mri in range(num_mr):

            MRJobId=mri
            cpu = self.rnd.random()/10
            prob = float(self.fileAccess[mri])/float(self.totalFileAccesses)
#ReduceResourceElements            self.MRusage.append({"cpuload" : cpu, "memorysize": 0.0, "memoryload": 0.0, "hdloadread": 0.0, "hdloadwrite": 0.0, "networkload": 1.0, "probability": prob})
            self.MRusage.append({"cpuload" : cpu, "networkload": 1.0, "probability": prob})
        



        
        #Para cada uno de los jobs MR que tengamos MRJobId, hemos de indicar el fichero sobre el que se van a ejecutar fileId. Y para cada
        #fichero sobre el que un MR se ejecute , debemos de indicar el identificador del fichero en el que se escribirn
        #los resultados parciales del task map "temp" y los resultados finales del task reduce "output"
        
        
        
        self.MapReduceFiles = {}
        self.blocksPerFile = []
        self.MagicFiles = {}
        
        
        #asigno un MR a cada inputfile
        for fi in range(num_files):
            MRJobId=fi
            fileId=fi*3
            inputSize = self.inputFileSizes[fi]
            tmpSize = self.tempFileSizes[fi]
            outputSize = self.outputFileSizes[fi]
            self.MapReduceFiles[MRJobId,fileId] = {"temp": fileId+1 ,"output": fileId+2}
            self.MagicFiles[fileId,fileId+1,fileId+2]={"readInput": [], "writeTemp": [], "readTemp": [], "writeOutput":[], "mr":MRJobId }
            self.blocksPerFile.append(inputSize)
            self.blocksPerFile.append(tmpSize)
            self.blocksPerFile.append(outputSize)

            
            
        #Para cada fichero que hemos definido anteriormente \all fileid + \all temp + \all output, hemos de indicar el tamaño
        # de cada uno de ellos self.blocksPerFile. El tamaño viene dado por el número de bloques que ocupará. Y el índice del list corresponde al id del fichero

        
#******************************************************************************************
#   END Definición de los ficheros, bloques y procesos MapReduce de nuestro experimento
#******************************************************************************************


        #Las variables siguientes no las tiene que definir el suario, las creamos para facilitar los cálculos, pero se crean a partir de las variables anteriormente definidas


        self.FilesPerTempFiles = {}
        self.FilesPerOutputFiles = {}


        for key in self.MapReduceFiles:
            fitem = self.MapReduceFiles[key]
            self.FilesPerTempFiles[fitem['temp']] = {"input" : key[1], "output": fitem['output']}
            self.FilesPerOutputFiles[fitem['output']] = {"input" : key[1], "temp": fitem['temp']}



        self.tempFiles = set()
        self.outputFiles = set()
        
        self.MRjobsPerInputFile = {} #a dictionary indexed by file id with the mapreduces that access to that fileid
        self.InputFilesPerMRJob = {} # indexed by mr id with the files that this MR accesses
        self.MRjobsPerOutTempFile = {}
        
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
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['temp']] = mrKey
            self.MRjobsPerOutTempFile[self.MapReduceFiles[(mrKey,fileKey)]['output']] = mrKey
 
                                                          
                                                           
                                                          