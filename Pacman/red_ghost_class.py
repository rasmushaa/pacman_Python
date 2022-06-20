'''
Created on 18 Jan 2020

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
class Red_ghost(Enemy):
    
    def __init__(self, app, grid_pos):
        Enemy.__init__(self, app, grid_pos)
        
        self.color      = RED_GHOST
        self.speed      = RED_GHOST_SPEED
        self.sprites    = self.app._sprites["red_ghost"]


    def find_target(self):
        
        if self.state == "scatter": 
            self.target = vec(1, 1)
        
        elif self.state == "chase": 
            self.target = self.app._player.grid_pos
            self.speed = RED_GHOST_SPEED * (1 + 0.00040 * (285 - len(self.app.coins)))
            
        elif self.state == "scared":
            self.speed = RED_GHOST_SPEED - 0.5 * RED_GHOST_SPEED 
            self.only_forward = False            
            self.target = self._initial_grid_pos
             
        return a_star.get_direction_to_target(self, self.target, self.grid_pos, self.only_forward)
    
    
    def update_scared_mode(self):
        if not self.not_eaten:
            self.speed = RED_GHOST_SPEED + 0.7 * RED_GHOST_SPEED 
        
        if self.grid_pos == self._initial_grid_pos:
            self.not_eaten = True
            self.speed = RED_GHOST_SPEED
            self.only_forward = True
            self.direction = vec(0, -1)
            self.state = "scatter"  
    
    
    def update_leave_castle(self):
        
        if len(self.app.coins) < 285:
            self.leave_castle = True
