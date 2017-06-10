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



dinour_f ='20170609135439'
statour_f = '20170609143356'
dinbad_f = '20170609152602'
statbad_f = '20170609163000'

datadir = './hdfs'


pkl_file = open(datadir+'/'+dinour_f+'/OBJECTIVEDYNAMICOURNETfitevolutions.pkl', 'rb')
dinour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statour_f+'/OBJECTIVESTATICOURNETfitevolutions.pkl', 'rb')
statour = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+dinbad_f+'/OBJECTIVEDYNAMICBADNETfitevolutions.pkl', 'rb')
dinbad = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open(datadir+'/'+statbad_f+'/OBJECTIVESTATICBADNETfitevolutions.pkl', 'rb')
statbad = pickle.load(pkl_file)
pkl_file.close()





font = {'size'   : 18}

matplotlib.rc('font', **font)


figtitleStr = 'network'

#seriesToPlot = ['min','mean','sfit']
#domainsToPlot = ['schdvar', 'schd', 'var', 'control']

seriesToPlot = ['min']
domainsToPlot = ['schdvar', 'schd', 'var', 'control']


    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
fig = plt.figure(figsize=(15,5))
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
fig.suptitle(figtitleStr, fontsize=18)
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
ax.set_xlabel('Generations', fontsize=18)
ax.set_ylabel('objectivo 0', fontsize=18)
plt.gcf().subplots_adjust(left=0.18)
plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    




if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinour[0]['sfit'], label='weighted schd+var', linestyle='--', linewidth=2.5,color='red',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
            ax.plot(dinour[0]['mean'], label='mean schd+var', linestyle=':', linewidth=2.5,color='red',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
            ax.plot(dinour[0]['min'], label='min schd+var', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)

if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statour[0]['sfit'], label='weighted schd', linestyle='--',linewidth=2.5,color='green',marker='*',markersize=10,markevery=10)
    if 'schdvar' in domainsToPlot:
        if 'mean' in seriesToPlot:
            ax.plot(statour[0]['mean'], label='mean schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
            ax.plot(statour[0]['min'], label='min schd', linewidth=2.5,color='green',marker='^',markersize=10,markevery=10)

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinbad[0]['sfit'], label='weighted var', linestyle='--',linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
            ax.plot(dinbad[0]['mean'], label='mean var', linestyle=':', linewidth=2.5,color='blue',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
            ax.plot(dinbad[0]['min'], label='min var', linewidth=2.5,color='blue',marker='^',markersize=10,markevery=10)

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statbad[0]['sfit'], label='weighted control', linestyle='--',linewidth=2.5,color='orange',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
            ax.plot(statbad[0]['mean'], label='mean control', linestyle=':', linewidth=2.5,color='orange',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
            ax.plot(statbad[0]['min'], label='min control', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=10)





plt.legend(loc="upper center", ncol=4, fontsize=14, bbox_to_anchor=(0.5, 1.5)) 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
#plt.legend()
   #    plt.show()

#if minYaxes[plotId]!= None:
#    plt.ylim(ymin=minYaxes[plotId])
   
   
plt.grid()
fig.savefig(datadir+'/network.pdf')
fig.show()
plt.close(fig)



figtitleStr = 'reliability'



    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
fig = plt.figure(figsize=(15,5))
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
fig.suptitle(figtitleStr, fontsize=18)
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
ax.set_xlabel('Generations', fontsize=18)
ax.set_ylabel('objectivo 0', fontsize=18)
plt.gcf().subplots_adjust(left=0.18)
plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    


if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinour[1]['sfit'], label='weighted schd+var', linestyle='--', linewidth=2.5,color='red',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(dinour[1]['mean'], label='mean schd+var', linestyle=':', linewidth=2.5,color='red',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(dinour[1]['min'], label='min schd+var', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statour[1]['sfit'], label='weighted schd', linestyle='--',linewidth=2.5,color='green',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(statour[1]['mean'], label='mean schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(statour[1]['min'], label='min schd', linewidth=2.5,color='green',marker='^',markersize=10,markevery=10)

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinbad[1]['sfit'], label='weighted var', linestyle='--',linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(dinbad[1]['mean'], label='mean var', linestyle=':', linewidth=2.5,color='blue',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(dinbad[1]['min'], label='min var', linewidth=2.5,color='blue',marker='^',markersize=10,markevery=10)

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statbad[1]['sfit'], label='weighted control', linestyle='--',linewidth=2.5,color='orange',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(statbad[1]['mean'], label='mean control', linestyle=':', linewidth=2.5,color='orange',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(statbad[1]['min'], label='min control', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=10)


plt.grid()
fig.savefig(datadir+'/reliability.pdf')
fig.show()
plt.close(fig)



figtitleStr = 'migration'

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
fig = plt.figure(figsize=(15,5))
   #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
fig.suptitle(figtitleStr, fontsize=18)
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.15)
   #    ax.set_title('axes title')
ax.set_xlabel('Generations', fontsize=18)
ax.set_ylabel('objectivo 0', fontsize=18)
plt.gcf().subplots_adjust(left=0.18)
plt.gcf().subplots_adjust(right=0.95)



#ax.plot(statbad[0]['max'], label='max', linewidth=2.5,color='yellow',marker='*',markersize=10,markevery=10)
#ax.plot(statbad[0]['mean'], label='mean', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
#ax.plot(statbad[0]['min'], label='min', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)
#ax.plot(mydataSerie['sfit'], label='weighted', linewidth=2.5,color='blue',marker='s',markersize=10,markevery=10)    


if 'schdvar' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinour[2]['sfit'], label='weighted schd+var', linestyle='--', linewidth=2.5,color='red',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(dinour[2]['mean'], label='mean schd+var', linestyle=':', linewidth=2.5,color='red',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(dinour[2]['min'], label='min schd+var', linewidth=2.5,color='red',marker='^',markersize=10,markevery=10)

if 'schd' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statour[2]['sfit'], label='weighted schd', linestyle='--',linewidth=2.5,color='green',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(statour[2]['mean'], label='mean schd', linestyle=':', linewidth=2.5,color='green',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(statour[2]['min'], label='min schd', linewidth=2.5,color='green',marker='^',markersize=10,markevery=10)

if 'var' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(dinbad[2]['sfit'], label='weighted var', linestyle='--',linewidth=2.5,color='blue',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(dinbad[2]['mean'], label='mean var', linestyle=':', linewidth=2.5,color='blue',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(dinbad[2]['min'], label='min var', linewidth=2.5,color='blue',marker='^',markersize=10,markevery=10)

if 'control' in domainsToPlot:
    if 'sfit' in seriesToPlot:
        ax.plot(statbad[2]['sfit'], label='weighted control', linestyle='--',linewidth=2.5,color='orange',marker='*',markersize=10,markevery=10)
    if 'mean' in seriesToPlot:
        ax.plot(statbad[2]['mean'], label='mean control', linestyle=':', linewidth=2.5,color='orange',marker='o',markersize=10,markevery=10)
    if 'min' in seriesToPlot:
        ax.plot(statbad[2]['min'], label='min control', linewidth=2.5,color='orange',marker='^',markersize=10,markevery=10)


plt.grid()
fig.savefig(datadir+'/migration.pdf')
fig.show()
plt.close(fig)
