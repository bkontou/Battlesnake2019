import json
import os
import random
import bottle
import time

from api import ping_response, start_response, move_response, end_response



class Queue:
    def __init__(self):
        self.q = []
    
    def put(self, obj):
        self.q.append(obj)
    
    def get(self):
        obj = self.q[len(self.q)-1]
        self.q.pop(len(self.q)-1)
        return obj




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
    

class Tree:
    def __init__(self, cargo, up=None, down=None, left=None, right=None, prev=None):
        self.cargo = cargo
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.prev = prev
        
        
def search_tree(T_H):
    Q = Queue()
    Q.put(T_H)
    path = []
    path.append
    
    while not Q.empty():
        T = Q.get()
        
        if T.up:
            Q.put(T.up)
        if T.down:
            Q.put(T.down)
        if T.left:
            Q.put(T.left)
        if T.right:
            Q.put(T.right)
            
def BFS(T_H,l):
    Q = Queue()
    
    Q.put(T_H)
    
    while not Q.empty():
        T = Q.get()
        
        if T.cargo == l:
            #print("ladies and gentlemen... we got em")
            return get_path(T)
        
        if T.up:
            Q.put(T.up)
        if T.down:
            Q.put(T.down)
        if T.left:
            Q.put(T.left)
        if T.right:
            Q.put(T.right)
    
    return None

def get_path(T):
    path = []
    
    path.append(T.cargo)
    N = T.prev
    while N != None:
        path.append(N.cargo)
        N = N.prev
    
    return path

        

def build_tree(M,H_L):
    loc_list = []
            
    T_H = Tree(H_L)
    up = T_H.cargo.update_x(-1)
    down = T_H.cargo.update_x(1)
    left = T_H.cargo.update_y(-1)
    right = T_H.cargo.update_y(1)
    loc_list.append(T_H.cargo)
    
    Q = Queue()
    
    
    try:
        if M[up.x][up.y] != 1 and (up.x >= 0 and up.y >= 0):
            T_H.up = Tree(up, prev=T_H)
            Q.put(T_H.up)
            loc_list.append(up)
    except:
        pass
    try:
        if M[down.x][down.y] != 1 and (down.x >= 0 and down.y >= 0):
            T_H.down = Tree(down, prev=T_H)
            Q.put(T_H.down)
            loc_list.append(down)
    except:
        pass
    try:
        if M[left.x][left.y] != 1 and (left.x >= 0 and left.y >= 0):
            T_H.left = Tree(left, prev=T_H)
            Q.put(T_H.left)
            loc_list.append(left)
    except:
        pass
    try:
        if M[right.x][right.y] != 1 and (right.x >= 0 and right.y >= 0):
            T_H.right = Tree(right, prev=T_H)
            Q.put(T_H.right)
            loc_list.append(right)
    except:
        pass
    
    
    
    n = 0

    while not Q.empty():
        n+=1
        
        T = Q.get()
        
        up = T.cargo.update_x(-1)
        down = T.cargo.update_x(1)
        left = T.cargo.update_y(-1)
        right = T.cargo.update_y(1)
    
        try:
            if M[up.x][up.y] != 1 and (up.x >= 0 and up.y >= 0) and up not in loc_list:
                T.up = Tree(up, prev=T)
                Q.put(T.up)
                loc_list.append(up)
        except:
            pass
            
        try:
            if M[down.x][down.y] != 1 and (down.x >= 0 and down.y >= 0) and down not in loc_list:
                T.down = Tree(down, prev=T)
                Q.put(T.down)
                loc_list.append(down)
        except:
            pass
            
        try:
            if M[left.x][left.y] != 1 and (left.x >= 0 and left.y >= 0) and left not in loc_list:
                T.left = Tree(left, prev=T)
                Q.put(T.left)
                loc_list.append(left)
        except:
            pass
            
        try:
            if M[right.x][right.y] != 1 and (right.x >= 0 and right.y >= 0) and right not in loc_list:
                T.right = Tree(right, prev=T)
                Q.put(T.right)
                loc_list.append(right)
        except:
            pass
        
    return T_H
        
    
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
    M = []
    
    data = bottle.request.json
        
    H, W = data["board"]["height"], data["board"]["height"]
    
    
    global state
    global snakesizeinit
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
    
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
        
    my_snake_body = to_loc_list(data["you"]["body"])

    snake_head = my_snake_body[0]
    
    food = to_loc_list(data["board"]["food"])

    #find closest food to head
    m = 5000 
    closest = Loc(0,0)
    for i,f in enumerate(food):
        if (f-snake_head).dist() < m:
            m = (f-snake_head).dist()
            closest = f
    
    
    #compile all snakes into 1 list
    snakelist = []
    for snake in data["board"]["snakes"]:
        snakelist += snake["body"]
    
    snakelist = to_loc_list(snakelist)
    snakelist.remove(my_snake_body[len(my_snake_body)-1])

    #print("updating map")
    #update map with snakes
    for i in range(H):
        for j in range(W):
            M[j][i] = 0
    
    for s in snakelist:
        M[s.x][s.y] = 1
    
    #build tree over map. tree head is snake head
    T_H = build_tree(M, snake_head)
        
    #idea: if snake gets to a cross road, break map into two and sum 1s in
    #each side to see which side it should take: pro tip: take the lower sum side
    if state == 'feed':
        path = BFS(T_H,closest)
        
        if path == None:
            for i,f in enumerate(food):
                path = BFS(T_H,f)
                if path != None:
                    break
        if path == None:
            for i in range(H):
                for j in range(W):
                    M[i][j] = 0
            for s in snakelist:
                M[s.x][s.y] = 1
            
            path = BFS(T_H,closest)
        
        if path == None or len(my_snake_body) >= snakesizeinit+2:
            state = 'chase'
    
    elif state == 'chase':
        print("chasing tail")
        path = BFS(T_H, my_snake_body[len(my_snake_body)-1])
        
        if data["you"]["health"] < 40:
            snakesizeinit = len(my_snake_body)
            state = 'feed'
    

    
    direction = 'down'
    
    if path == None:
        #This shit is fucked!!! Need to rewrite!
        print("cant find path!!!!")
        d = my_snake_body[1] - my_snake_body[0]
        
        p_next = snake_head + d
        
        if p_next.x >= W-1 or p_next.x <= 0 or p_next.y >= H-1 or p_next.y <= 0:
            n = 0
            #print("gunna hit a wall")
            if p_next in my_snake_body:
                pass
                #print("OH NO")
            
            
        else:
            n = 0
            while p_next not in snakelist:
                p_next = snake_head + dirs[n]
                n+=1
        
        d = p_next - snake_head
        
        if d == dirs[0]:
            direction = 'up'
        if d == dirs[1]:
            direction = 'right'
        if d == dirs[2]:
            direction = 'down'
        if d == dirs[3]:
            direction = 'left'
                
    else:
        #Follow the first direction of the path you got from the BFS
        d = path[len(path)-2] - path[len(path)-1]
        print("direction:")
        print(d)
        
        if d.y > 0:
            direction = 'down'
        elif d.y < 0:
            direction = 'up'
        elif d.x > 0:
            direction = 'right'
        elif d.x < 0:
            direction = 'left'


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
