'''
Created on 16 Jan 2020

@author: rasmus
'''




import  pygame
from    enemy_class         import Enemy
from    A_star_heap_class   import *
from    settings            import *

a_star = A_star
vec = pygame.math.Vector2


''' Haamu-olio luodaan Ghost(app, vec(x,y))
    pelissa kutsutaan ensin Ghost.update()
    , mikä paivittaa kaiken ja
    sitten Ghost.draw(), mika piirtaa sen'''
class Blue_ghost(Enemy):
    
    def __init__(self, app, grid_pos):
        Enemy.__init__(self, app, grid_pos)
        
        self.color      = BLUE_GHOST
        self.speed      = BLUE_GHOST_SPEED
        self.sprites    = self.app._sprites["blue_ghost"]
        


    def find_target(self):
        
        if self.state == "scatter": 
            self.target = vec(21, 1)
        
        elif self.state == "chase": 
            
            self.target = self.app._player.grid_pos + self.app._player.direction * 5
            
            if self.target.x > CELL_X-1: self.target.x = CELL_X-1
            if self.target.x < 0: self.target.x = 0
            
            if self.target.y > CELL_Y-1: self.target.y = CELL_Y-1
            if self.target.y < 0: self.target.y = 0
            
        elif self.state == "scared":
            self.speed = BLUE_GHOST_SPEED - 0.5 * BLUE_GHOST_SPEED
            self.only_forward = False            
            self.target = self._initial_grid_pos
            
            
        return a_star.get_direction_to_target(self, self.target, self.grid_pos, self.only_forward)
    
    
    def update_scared_mode(self):
        if not self.not_eaten:
            self.speed = BLUE_GHOST_SPEED + 0.7 * BLUE_GHOST_SPEED
        
        if self.grid_pos == self._initial_grid_pos:
            self.speed = BLUE_GHOST_SPEED
            self.not_eaten = True
            self.only_forward = True
            self.direction = vec(0, -1)
            self.state = "scatter"  
    
    
    def update_leave_castle(self):
        
        if len(self.app.coins) < 250:
            self.leave_castle = True




            