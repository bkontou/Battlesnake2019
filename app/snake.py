# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:45:12 2019

@author: bkontou
"""

from graph import Loc

class Block(Loc):
    def __init__(self,x,y,sdict):
        self.x = x
        self.y = y
        
        self.keys = ['N','E','S','W','NE','NW','SE','SW']
        self.sides = {}
        for k in self.keys:
            if k in sdict:
                self.sides[k] = sdict[k]
            else:
                self.sides[k] = None
                
class Snake:
    def __init__(self, body, G):
        self.body = body
        self.keys = ['N','E','S','W','NE','NW','SE','SW']
        self.head = self.__build_block(body[0],G)
        self.tail = self.__build_block(body[len(body)-1],G)
    
    def __len__(self):
        return len(self.body)
    
    def update_body(self,body):
        self.body = body
        self.head = Block(body[0])
        self.tail = Block(body[len(body-1)])
    
    def __build_block(self, loc, G):
        sides = [Loc(0,-1),Loc(1,0),Loc(0,1),Loc(-1,0),Loc(1,-1),Loc(-1,-1),Loc(1,1),Loc(-1,1)]
        sdict = {}
        for s,k in zip(sides,self.keys):
            if loc+s in G.nodes:
                sdict[k] = loc+s
        
        return Block(loc.x,loc.y,sdict)
        