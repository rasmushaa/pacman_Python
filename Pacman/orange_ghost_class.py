'''
Created on 19 Jan 2020

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
class Orange_ghost(Enemy):
    
    def __init__(self, app, grid_pos):
        Enemy.__init__(self, app, grid_pos)
        
        self.color      = ORANGE_GHOST
        self.speed      = ORANGE_GHOST_SPEED
        self.sprites    = self.app._sprites["orange_ghost"]
        


    def find_target(self):
        
        if self.state == "scatter": 
            self.target = vec(21, 26)
        
        elif self.state == "chase": 
            if abs(self.grid_pos.x - self.app._player.grid_pos.x) + abs(self.grid_pos.y - self.app._player.grid_pos.y) > 10:
                self.target = self.app._player.grid_pos
            else:
                self.target = vec(21, 26)
                
        elif self.state == "scared":
            self.speed = ORANGE_GHOST_SPEED - 0.5 * ORANGE_GHOST_SPEED
            self.only_forward = False            
            self.target = self._initial_grid_pos
               
        return a_star.get_direction_to_target(self, self.target, self.grid_pos, self.only_forward)
    
    
    def update_scared_mode(self):
        if not self.not_eaten:
            self.speed = ORANGE_GHOST_SPEED + 0.7 * ORANGE_GHOST_SPEED
        
        if self.grid_pos == self._initial_grid_pos:
            self.speed = ORANGE_GHOST_SPEED
            self.not_eaten = True
            self.only_forward = True
            self.direction = vec(0, -1)
            self.state = "scatter"  
        
    

    def update_leave_castle(self):
        
        if self.app._level < 2:
            if len(self.app.coins) < 150:
                self.leave_castle = True
                
        elif self.app._level < 3:
            if len(self.app.coins) < 200:
                self.leave_castle = True
                
        else:
            if len(self.app.coins) < 220:
                self.leave_castle = True
                
                