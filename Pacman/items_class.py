'''
Created on 22 Jan 2020

@author: rasmus
'''




import  pygame 
vec = pygame.math.Vector2


class Item():
    
    def __init__(self, app, grid_pos, name):
        self.app        = app
        self.grid_pos   = grid_pos
        self.not_eaten  = True
        self.item_type  = name
        
    def __eq__(self, grid_pos):
        if self.grid_pos == grid_pos:
            return True
        else:
            return False
        