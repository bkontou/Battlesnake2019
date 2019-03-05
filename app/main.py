import json
import os
import random
import bottle
import time

from api import ping_response, start_response, move_response, end_response

from Queue import Queue
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
            
            for E in G.edges[N]:
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
                
            
    

class Block(Loc):
    def __init__(self,x,y,up=None,down=None,left=None,right=None):
        self.x = x
        self.y = y
        
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        
class Snake:
    def ___init__(self, body, Head=None, Tail=None):
        self.body = body
        self.head = Block(body[0])
        self.tail = Block(body[len(body-1)])
    
    def __len__(self):
        return len(body)
    
    def update_body(self,body):
        self.body = body
        self.head = Block(body[0])
        self.tail = Block(body[len(body-1)])
        

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
             
    
def to_loc_list(locs):
    loc_list = []
    
    for l in locs:
        loc_list.append(Loc(l['x'],l['y']))
        
    return loc_list
    
    
    

# =============================================================================
# 
# print("initializing")
# for i in range(H):
#     a = []
#     for j in range(W):
#         a.append(0)
#     M.append(a)
# =============================================================================

#mysnake = snake([0],1)

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    
    #       up        right    down     left
    global dirs
    dirs = [Loc(-1,0),Loc(0,1),Loc(1,0),Loc(0,-1)]
    global M
    global H
    global W
    
    
    data = bottle.request.json
        
    H, W = data["board"]["height"], data["board"]["height"]
    
    M = np.zeros((H,W),dtype=int)
    
    
    global state
    global snakesizeinit
    global no_food
    no_food = 0
    snakesizeinit = len(data["you"]["body"])
    state = 'feed'
    
    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    global state
    global snakesizeinit
    global dirs
    global M
    global H
    global W
    global no_food
    global G
    H, W = data["board"]["height"], data["board"]["height"]
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
        
    my_snake_body = to_loc_list(data["you"]["body"])

    snake_head = my_snake_body[0]
    if len(my_snake_body) > 1:
        snake_head_direction = my_snake_body[0] - my_snake_body[1]
    else:
        snake_head_direction = Loc(0,1)
    
    food = to_loc_list(data["board"]["food"])
    

    #find closest food to head
    fooddists = []
    for f in food:
        fooddists.append(f-snake_head)
    fooddists = np.sort(fooddists)
    for i,f in enumerate(fooddists):
        fooddists[i] = f + snake_head 
    closest = fooddists[0]
    
    
    #compile all snakes into 1 list
    snakelist = []
    for snake in data["board"]["snakes"]:
        snakelist += snake["body"]
    
    snakelist = to_loc_list(snakelist)
    snakelist.remove(my_snake_body[len(my_snake_body)-1])
    snakelist.remove(my_snake_body[0])

    #print("updating map")
    #update map with snakes
    M = np.zeros((H,W),dtype=int)
    
    for s in snakelist:
        M[s.x,s.y] = 1
    for f in food:
        M[f.x,f.y] = 2
    
    #build tree over map. tree head is snake head
    G = build_graph(M)
    
    #check infront
    print(snake_head_direction)
    if snake_head + snake_head_direction not in G.nodes:
        LHS = snake_head + Loc(snake_head_direction.y,-1*snake_head_direction.x)
        RHS = snake_head + Loc(-1*snake_head_direction.y,snake_head_direction.x)
        
        
        RHS_n = floodfill(G.remove_node(snake_head),RHS)
        LHS_n = floodfill(G.remove_node(snake_head),LHS)
        
        if RHS_n > LHS_n:
            if RHS_n < len(my_snake_body):
                print("AAA")
                #chase tail
            for f in fooddists:
                if G.floodfind(RHS,f):
                    closest = f
                else:
                    pass
        elif LHS_n > RHS_n:
            if LHS_n < len(my_snake_body):
                print("AAA")
                #chase tail
            for f in fooddists:
                if G.floodfind(RHS,f):
                    closest = f
                else:
                    pass
        elif RHS_n == LHS_n:
            print("yeeT")
    
    path =  Astar(G,snake_head, closest)
    direction = 'down'

    if path != None:
        if len(path) < 2:
            d = Loc(1,0)
        else:
            d = path[1] - path[0]

        print("finding")
        if d.y > 0:
            direction = 'down'
            print('down')
        elif d.y < 0:
            direction = 'up'
            print('u')
        elif d.x > 0:
            direction = 'right'
            print('r')
        elif d.x < 0:
            direction = 'left' 
            print('l')
    else:
        print("cant find path")
       

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
