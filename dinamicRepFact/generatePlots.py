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


pkl_file = open(datadir+'/'+dinour_f+'/'+nodenumber+'OBJECTIVEDYNAMICOURNETfitevolutions.pkl', 'rb')
dinour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statour_f+'/'+nodenumber+'OBJECTIVESTATICOURNETfitevolutions.pkl', 'rb')
statour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+dinbad_f+'/'+nodenumber+'OBJECTIVEDYNAMICBADNETfitevolutions.pkl', 'rb')
dinbad = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statbad_f+'/'+nodenumber+'OBJECTIVESTATICBADNETfitevolutions.pkl', 'rb')
statbad = pickle.load(pkl_file)
pkl_file.close()



allcases = [dinour,statour, dinbad, statbad]

limit = 61
for i in allcases:
    for j in i:
        for k in j:
            if len(j[k])>limit:
                j[k] = j[k][:limit]
            else:
                lastValue = j[k][len(j[k])-1]
                while len(j[k])<limit:
                    j[k].append(lastValue)


#
#limit = 60
#dinour[0]['min'] = dinour[0]['min'][:limit]
#dinour[0]['mean'] = dinour[0]['mean'][:limit]
#dinour[0]['sfit'] = dinour[0]['sfit'][:limit]
#
#dinour[1]['min'] = dinour[1]['min'][:limit]
#dinour[1]['mean'] = dinour[1]['mean'][:limit]
#dinour[1]['sfit'] = dinour[1]['sfit'][:limit]
#
#dinour[2]['min'] = dinour[2]['min'][:limit]
#dinour[2]['mean'] = dinour[2]['mean'][:limit]
#dinour[2]['sfit'] = dinour[2]['sfit'][:limit]
#
#dinour[3]['min'] = dinour[3]['min'][:limit]
#dinour[3]['mean'] = dinour[3]['mean'][:limit]
#dinour[3]['sfit'] = dinour[3]['sfit'][:limit]
#
#statour[0]['min'] = statour[0]['min'][:limit]
#statour[0]['mean'] = statour[0]['mean'][:limit]
#statour[0]['sfit'] = statour[0]['sfit'][:limit]
#
#statour[1]['min'] = statour[1]['min'][:limit]
#statour[1]['mean'] = statour[1]['mean'][:limit]
#statour[1]['sfit'] = statour[1]['sfit'][:limit]
#
#statour[2]['min'] = statour[2]['min'][:limit]
#statour[2]['mean'] = statour[2]['mean'][:limit]
#statour[2]['sfit'] = statour[2]['sfit'][:limit]
#
#statour[3]['min'] = statour[3]['min'][:limit]
#statour[3]['mean'] = statour[3]['mean'][:limit]
#statour[3]['sfit'] = statour[3]['sfit'][:limit]
#
#dinbad[0]['min'] = dinbad[0]['min'][:limit]
#dinbad[0]['mean'] = dinbad[0]['mean'][:limit]
#dinbad[0]['sfit'] = dinbad[0]['sfit'][:limit]
#
#dinbad[1]['min'] = dinbad[1]['min'][:limit]
#dinbad[1]['mean'] = dinbad[1]['mean'][:limit]
#dinbad[1]['sfit'] = dinbad[1]['sfit'][:limit]
#
#dinbad[2]['min'] = dinbad[2]['min'][:limit]
#dinbad[2]['mean'] = dinbad[2]['mean'][:limit]
#dinbad[2]['sfit'] = dinbad[2]['sfit'][:limit]
#
#dinbad[3]['min'] = dinbad[3]['min'][:limit]
#dinbad[3]['mean'] = dinbad[3]['mean'][:limit]
#dinbad[3]['sfit'] = dinbad[3]['sfit'][:limit]
#
#statbad[0]['min'] = statbad[0]['min'][:limit]
#statbad[0]['mean'] = statbad[0]['mean'][:limit]
#statbad[0]['sfit'] = statbad[0]['sfit'][:limit]
#
#statbad[1]['min'] = statbad[1]['min'][:limit]
#statbad[1]['mean'] = statbad[1]['mean'][:limit]
#statbad[1]['sfit'] = statbad[1]['sfit'][:limit]
#
#statbad[2]['min'] = statbad[2]['min'][:limit]
#statbad[2]['mean'] = statbad[2]['mean'][:limit]
#statbad[2]['sfit'] = statbad[2]['sfit'][:limit]
#
#statbad[3]['min'] = statbad[3]['min'][:limit]
#statbad[3]['mean'] = statbad[3]['mean'][:limit]
#statbad[3]['sfit'] = statbad[3]['sfit'][:limit]



font = {'size'   : 18}

matplotlib.rc('font', **font)


figtitleStr = 'network'

#seriesToPlot = ['min','mean','sfit']
#domainsToPlot = ['schdvar', 'schd', 'var', 'control']

seriesToPlot = ['mean']
domainsToPlot = ['schdvar', 'schd', 'var', 'control']



fig, (ax1,ax2,ax3) = plt.subplots(3,1, sharex=True,figsize=(15,15))
   
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
#fig = plt.figure(figsize=(15,15),sharex=True)
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
#fig.suptitle(figtitleStr, fontsize=18)

#ax1 = fig.add_subplot(311)
#fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
#ax1.set_xlabel('Generations', fontsize=18)
ax1.set_ylabel('Mean Network Latency (s)', fontsize=18)
#plt.gcf().subplots_adjust(left=0.18)
#plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    




if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax1.plot(dinour[0]['sfit'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax1.plot(dinour[0]['mean'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=slice(2,100,10))
    if 'min' in seriesToPlot:
        ax1.plot(dinour[0]['min'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=10)

if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax1.plot(statour[0]['sfit'], label='schd', linestyle=':',linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))
    if 'mean' in seriesToPlot:
        ax1.plot(statour[0]['mean'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))
    if 'min' in seriesToPlot:
        ax1.plot(statour[0]['min'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax1.plot(dinbad[0]['sfit'], label='var',linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))
    if 'mean' in seriesToPlot:
        ax1.plot(dinbad[0]['mean'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))
    if 'min' in seriesToPlot:
        ax1.plot(dinbad[0]['min'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax1.plot(statbad[0]['sfit'], label='control', linestyle='-.',linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'mean' in seriesToPlot:
        ax1.plot(statbad[0]['mean'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'min' in seriesToPlot:
        ax1.plot(statbad[0]['min'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))





ax1.legend(loc="upper center", ncol=4, fontsize=14, bbox_to_anchor=(0.5, 1.2)) 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
#plt.legend()
   #    plt.show()

#if minYaxes[plotId]!= None:
#    plt.ylim(ymin=minYaxes[plotId])
   
   
plt.grid()
#fig.savefig(datadir+'/'+nodenumber+'network.pdf')
#fig.show()
#plt.close(fig)



figtitleStr = 'reliability'



    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
#fig = plt.figure(figsize=(15,5))
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
#fig.suptitle(figtitleStr, fontsize=18)
#ax2 = fig.add_subplot(312)
#fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
#ax2.set_xlabel('Generations', fontsize=18)
ax2.set_ylabel('Failure Rate (failure/hour)', fontsize=18)
#plt.gcf().subplots_adjust(left=0.18)
#plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    


if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        l2,=ax2.plot(dinour[1]['sfit'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=slice(2,100,10))
    if 'mean' in seriesToPlot:
        l2,=ax2.plot(dinour[1]['mean'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=slice(2,100,10))
    if 'min' in seriesToPlot:
        l2,=ax2.plot(dinour[1]['min'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=slice(2,100,10))
if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        l2,=ax2.plot(statour[1]['sfit'], label='schd', linestyle=':',linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(5,100,10))
    if 'mean' in seriesToPlot:
        l2,=ax2.plot(statour[1]['mean'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(5,100,10))
    if 'min' in seriesToPlot:
        l2,=ax2.plot(statour[1]['min'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(5,100,10))

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        l2,=ax2.plot(dinbad[1]['sfit'], label='var',linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        l2,=ax2.plot(dinbad[1]['mean'], label='var',  linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        l2,=ax2.plot(dinbad[1]['min'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        l2,=ax2.plot(statbad[1]['sfit'], label='control', linestyle='-.',linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'mean' in seriesToPlot:
        l2,=ax2.plot(statbad[1]['mean'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'min' in seriesToPlot:
        l2,=ax2.plot(statbad[1]['min'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))


plt.grid()
#fig.savefig(datadir+'/'+nodenumber+'reliability.pdf')
#fig.show()
#plt.close(fig)



figtitleStr = 'migration'

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
#fig = plt.figure(figsize=(15,5))
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
#fig.suptitle(figtitleStr, fontsize=18)
#ax3 = fig.add_subplot(313)
#fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
ax3.set_xlabel('Generations', fontsize=18)
ax3.set_ylabel('Mean Migration Cost (s)', fontsize=18)
#plt.gcf().subplots_adjust(left=0.18)
#plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    


if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax3.plot(dinour[2]['sfit'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax3.plot(dinour[2]['mean'], label='schd+var', linestyle='--', linewidth=2.5,color='red',marker='s',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax3.plot(dinour[2]['min'], label='schd+var', linestyle='--',linewidth=2.5,color='red',marker='s',markersize=10,markevery=10)

if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax3.plot(statour[2]['sfit'], label='schd', linestyle=':',linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))
    if 'mean' in seriesToPlot:
        ax3.plot(statour[2]['mean'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))
    if 'min' in seriesToPlot:
        ax3.plot(statour[2]['min'], label='schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=slice(2,100,10))

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax3.plot(dinbad[2]['sfit'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))
    if 'mean' in seriesToPlot:
        ax3.plot(dinbad[2]['mean'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))
    if 'min' in seriesToPlot:
        ax3.plot(dinbad[2]['min'], label='var', linewidth=2.5,color='blue',marker='*',markersize=10,markevery=slice(5,100,10))

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax3.plot(statbad[2]['sfit'], label='control', linestyle='-.',linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'mean' in seriesToPlot:
        ax3.plot(statbad[2]['mean'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))
    if 'min' in seriesToPlot:
        ax3.plot(statbad[2]['min'], label='control', linestyle='-.', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=slice(8,100,10))


ax1.grid()
ax2.grid()
ax3.grid()
fig.savefig(datadir+'/'+nodenumber+'.pdf')
fig.show()
#plt.close(fig)
