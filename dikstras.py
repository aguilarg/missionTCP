#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 23:07:34 2018

@author: gracielaaguilar
"""
import networkx as nx
import numpy as np
#fix distance 
graph = np.array([[0,4,3,0,7,0,0,0],[4,0,6,0,0,0,0,5], [3,6,0,11,0,0,0,0],
          [0,0,11,0,0,6,10,9], [7,0,0,0,0,0,5,0], [0,0,0,6,0,0,0,5],
          [0,0,0,10,5,0,0,0],[0,5,0,9,0,5,0,0]])
G = nx.from_numpy_matrix(graph, create_using=nx.DiGraph())
def dijAlg(route, node):
    
    print("for Router",route[node], ":")
    
    
    print("Destination      Distance       Shortest Path")
    for i in range(8):
        
        result = []
        path = nx.dijkstra_path(G, node, i)
        ix =[[path[i],path[i+1]] for i in range(len(path)-1)]
        total = sum([graph[i[0]][i[1]] for i in ix])
        for j in range (0, len(path)):
            num = path[j]
            
            #print(counter)
            result.append(route[num])    
        print(route[i],"               ", total, "             ", result)
        total = 0
 
    
annToChan = []
annToJan = []

chanToAnn = []
chanToJan = []

janToAnn = []
janToChan = []

fp = open('Ann-_Chan.txt') 
annToChan = fp.read().split("\n") 
fp.close() 
fp = open('Ann-_Jan.txt') 
annToJan = fp.read().split("\n") 
fp.close() 

fp = open('Chan-_Ann.txt') 
chanToAnn = fp.read().split("\n") 
fp.close() 
fp = open('Chan-_Jan.txt') 
chanToJan = fp.read().split("\n") 
fp.close() 

fp = open('Jan-_Ann.txt') 
janToAnn = fp.read().split("\n") 
fp.close() 
fp = open('Jan-_Chan.txt') 
janToChan = fp.read().split("\n") 
fp.close() 


routers = ['A','B','C','D','E','F','G','L']

#G = nx.from_numpy_matrix(graph, create_using=nx.DiGraph())

dijAlg (routers, 0)
dijAlg (routers, 1)
dijAlg (routers, 2)
dijAlg (routers, 3)
dijAlg (routers, 4)
dijAlg (routers, 5)
dijAlg (routers, 6)
dijAlg (routers, 7)




