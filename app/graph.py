# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:04:05 2019

@author: bkontou
"""

from queue import Queue
from copy import deepcopy as copy

import numpy as np
from collections import defaultdict

class Loc:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def update_x(self,n):
        return Loc(self.x + n, self.y)
    
    def update_y(self,n):
        return Loc(self.x, self.y + n)
    
    def dist(self):
        return self.x**2 + self.y**2
    
    def __add__(self, L):
        return Loc(self.x + L.x, self.y + L.y)
    
    def __sub__(self, L):
        return Loc(self.x - L.x, self.y - L.y)
    
    def __str__(self):
        return("(%d,%d)"%(self.x,self.y))

    def __eq__(self, L):
        if self.x == L.x and self.y == L.y:
            return True
        else:
            return False
    
    def __gt__(self,L):
        if self.dist() > L.dist():
            return True
        else:
            return False
    
    def __ls__(self,L):
        if self.dist() < L.dist():
            return True
        else:
            return False
    
    def __gte__(self,L):
        if self.dist() >= L.dist():
            return True
        else:
            return False
    
    def __lse__(self,L):
        if self.dist() <= L.dist():
            return True
        else:
            return False
        
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        return hash((self.x,self.y))

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
    
    def add_node(self, node):
        self.nodes.add(node)
    
    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        
    def remove_edge(self, from_node, to_node):
        removed = copy(self)
        try:
            del removed.edges[from_node]
            del removed.edges[to_node]
        except:
            print("edge does not exist")
        return removed
        
    def remove_node(self, node):
        removed = copy(self)
        for E in self.edges[node]:
            removed = removed.remove_edge(node,E)
        try:
            removed.nodes.remove(node)
        except:
            print("node does not exist")
        
        return removed
    
    def floodfind(self, From, L):
        Q = Queue()
        
        if From not in self or L not in self:
            return False
    
        Q.put(From)
        to_visit = [From]
        
        while not Q.empty():
            N = Q.get()
            if N == L:
                return True
            
            for E in self.edges[N]:
                if E not in to_visit:
                    to_visit.append(E)
                    Q.put(E)
                
        return False
        
    
    def __contains__(self,L):
        return L in self.nodes
            
def build_graph(M):
    G = Graph()
    
    for i, I in enumerate(M):
        for j, J in enumerate(I):
            if M[i,j] != 1:
                G.add_node(Loc(i,j))
            
    for N in G.nodes:
        i = N.x
        j = N.y
        try:
            if M[i+1,j] != 1:
                G.add_edge(Loc(i,j),Loc(i+1,j))
        except:
            pass
        
        try:
            if M[i,j+1] != 1:
                G.add_edge(Loc(i,j),Loc(i,j+1))
        except:
            pass
            
            
    return G

class Node(Loc):
    def __init__(self,x,y,parent=None):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        

def Astar(G,start,end):
    
    openList = []
    closedList = []
    
    startNode = Node(start.x,start.y)
    endNode = Node(end.x,end.y)
    
    openList.append(startNode)
    
    while len(openList) > 0:
        current = openList[0]
        c_index = 0
        for index, item in enumerate(openList):
            if item.f < current.f:
                current = item
                c_index = index
        
        openList.pop(c_index)
        closedList.append(current)
        
        if current == end:
            #get path
            path = []
            c = current
            while c is not None:
                path.append(Loc(c.x,c.y))
                c = c.parent
            return path[::-1]
        
        children = []
        for node in G.edges[current]:
            children.append(Node(node.x,node.y,parent=current))
        
        for child in children:
            if child in closedList:
                continue
            
            child.g = current.g + 1
            child.h = (end - child).dist()
            child.f = child.g + child.h
            
            if child in openList:
                if child.g > openList[openList.index(child)].g:
                    continue
            
            openList.append(child)
                
            
    
        

def floodfill(G, H):
    Q = Queue()
    
    if H not in G:
        return 0
    
    Q.put(H)
    to_visit = [H]
    n = 0
    
    while not Q.empty():
        N = Q.get()
        n+=1
        
        for E in G.edges[N]:
            if E not in to_visit:
                to_visit.append(E)
                Q.put(E)
            
    return n - 1
             

M = np.zeros((10,10))
M[0,0:5] = 1
M[0:5,5] = 1

G = build_graph(M)

