#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:45:24 2017

@author: carlos
"""

import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

from pylab import figure, title, xlabel, ylabel, xticks, bar, \
                  legend, axis, savefig, grid



dinour_f ='1'
statour_f = '2'
dinbad_f = '3'
statbad_f = '4'

nodenumber='32'

datadir = './hdfs'+nodenumber


pkl_file = open(datadir+'/'+dinour_f+'/'+nodenumber+'OBJECTIVEDYNAMICOURNETlastgeneration.pkl', 'rb')
dinour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statour_f+'/'+nodenumber+'OBJECTIVESTATICOURNETlastgeneration.pkl', 'rb')
statour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+dinbad_f+'/'+nodenumber+'OBJECTIVEDYNAMICBADNETlastgeneration.pkl', 'rb')
dinbad = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statbad_f+'/'+nodenumber+'OBJECTIVESTATICBADNETlastgeneration.pkl', 'rb')
statbad = pickle.load(pkl_file)
pkl_file.close()


resultsDomains = [dinour,statour,dinbad,statbad]



font = {'size'   : 18}

matplotlib.rc('font', **font)



#seriesToPlot = ['min','mean','sfit']
#domainsToPlot = ['schdvar', 'schd', 'var', 'control']


domainsToPlot = ['schdvar', 'schd', 'var', 'control']


fig = plt.figure(figsize=(15,15))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)



   
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
#fig = plt.figure(figsize=(15,15),sharex=True)
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
#fig.suptitle(figtitleStr, fontsize=18)

#ax1 = fig.add_subplot(311)
#fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
#ax1.set_xlabel('Generations', fontsize=18)
ax1.set_ylabel('File locality (s)', fontsize=18)
#plt.gcf().subplots_adjust(left=0.18)
#plt.gcf().subplots_adjust(right=0.95)


series = [['migration','network'],['reliability','network'],['migration','reliability']]
misaxs = [ax1,ax2,ax3]

for m in [0,1,2]:
    for j in [0,1,2,3]:    
        serieA = series[m][0]
        serieB=series[m][1]
        colors=['red','green','blue','orange']
        #while len(popT.fronts[f])!=0:
        
        thisfront = [resultsDomains[j].fitness[i] for i in resultsDomains[j].fronts[0]]
        
        #a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
        a = [thisfront[i][serieA] for i,v in enumerate(thisfront)]
        b = [thisfront[i][serieB] for i,v in enumerate(thisfront)]
        
        #ax1 = fig.add_subplot(111)
        
        misaxs[m].scatter(a, b, s=10, color=colors[j], marker="o")
        misaxs[m].set_xlabel(serieA)
        misaxs[m].set_ylabel(serieB)
        
        #ax1.annotate('a',(a,b))
    
plt.show()
fig.savefig(datadir+'/'+nodenumber+'kk.pdf')
#plt.close(fig)







