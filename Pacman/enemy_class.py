'''
Created on 15 Jan 2020

@author: rasmus
'''




import  pygame
from    settings        import *

vec = pygame.math.Vector2



class Enemy():
    def __init__(self, app, grid_pos):
          
        self.app                = app
        self._initial_grid_pos  = vec(grid_pos.x, grid_pos.y)
        self.__old_grid_pos     = vec(0, 0)
        self.grid_pos           = grid_pos
        self.__old_pix_pos      = vec(0, 0)
        self.pixel_pos          = self.get_pix_pos()     
        self.direction          = vec(0, -1)
        self.color              = (0, 0, 0)
        self.sprites            = []
        self.__draw_counter     = 0
        self.speed              = 1
        self.target             = vec(0, 0)
        self.state              = "scatter"
        self.not_eaten          = True
        self.leave_castle       = False
        self.only_forward       = True
        

    # Kaytetaan alaluokassa katsomaan saako hahmo lahtea aloituspaikasta
    def update_leave_castle(self):
        pass
    
    # Kohteen sijainti maaritellaan yksilollisesti alaluokassa
    def find_target(self):
        pass   
    
    # paivittaa kyseisen haamun pako-tilan alaluokassa
    def update_scared_mode(self):
        pass
    
    
    def update(self):
        
        # jos haamu ei ole lahtenyt linnasta -> tarkista voiko lahtea
        if not self.leave_castle:
            self.update_leave_castle()

        # jos haamu ei pelkaa -> paivita tila levelin ja timerin mukaan, muuten paivita pako-tila
        if self.state != "scared":
            if self.app._level < 2:
                if self.app.timer < 10000: 
                    self.state = "scatter"
                elif self.app.timer < 30000: 
                    self.state = "chase"      
                              
            elif self.app._level < 3:
                if self.app.timer < 7000: 
                    self.state = "scatter"
                elif self.app.timer < 30000: 
                    self.state = "chase"            
            else:
                if self.app.timer < 2000: 
                    self.state = "scatter"
                elif self.app.timer < 30000: 
                    self.state = "chase"
                    
        else:
            self.update_scared_mode()


        # Paivittaa solun sijainnin
        self.grid_pos[0] = (self.pixel_pos[0] - TOP_BOTTOM_BUFFER + self.app._cell_width//2)   // self.app._cell_width + 1
        self.grid_pos[1] = (self.pixel_pos[1] - TOP_BOTTOM_BUFFER + self.app._cell_height//2) // self.app._cell_height + 1
            
        # Liikuttaa hahmoa
        if self.leave_castle:
            if self.on_the_center():
                if self.if_cross_section():
                    direction_to_target = self.find_target()           
                    if direction_to_target == vec(0, 0):
                        self.move()             
                    else:
                        self.direction = direction_to_target
                else:
                    self.move()
                
            self.pixel_pos += self.direction * self.speed
            
            # Paivittaa piirtolaskurin
            if abs(self.__old_pix_pos.x - self.pixel_pos.x) > self.app._cell_width*0.8 or abs(self.__old_pix_pos.y - self.pixel_pos.y) > self.app._cell_height*0.8:
                self.__old_pix_pos = self.get_pix_pos()
                self.__draw_counter += 1
                if self.__draw_counter > 1:
                    self.__draw_counter = 0
                    

    def move(self):
        for direction in POSSIBLE_DIRECTIONS:
            if self.get_revesre_direction() != direction:
                if self.can_move(direction, self.grid_pos):
                    self.direction = direction
                    break
    
    
    def can_move(self, dir, grid_pos):
        if vec(dir + grid_pos) not in self.app._walls:
            return True
        return False        
                       
            
    # tarkistaa onko vihollinen talla hetkella risteyksessa, vahintaan 3 suuntaa
    def if_cross_section(self):
        counter = 0
        for dir in POSSIBLE_DIRECTIONS:
            if vec(self.grid_pos + dir) not in self.app._walls: counter += 1      
        if counter >= 3: 
            return True   
        return False

            
            
    def on_the_center(self):
        if int(self.pixel_pos.x - TOP_BOTTOM_BUFFER//2) % self.app._cell_width < self.app._cell_width//5:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                if self.grid_pos != self.__old_grid_pos:
                    
                    self.__old_grid_pos.x = self.grid_pos.x
                    self.__old_grid_pos.y = self.grid_pos.y
                    
                    self.pixel_pos = self.get_pix_pos()
                    return True
            
        if int(self.pixel_pos.y - TOP_BOTTOM_BUFFER//2) % self.app._cell_height < self.app._cell_height//5:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                if self.grid_pos != self.__old_grid_pos:
                    
                    self.__old_grid_pos.x = self.grid_pos.x
                    self.__old_grid_pos.y = self.grid_pos.y
                    
                    self.pixel_pos = self.get_pix_pos()
                    return True

    
    
    def draw(self):
        if self.state != "scared":
            if self.direction == vec(1, 0):
                self.app._screen.blit(self.sprites[self.__draw_counter], (int(self.pixel_pos.x), int(self.pixel_pos.y)))          
            elif self.direction == vec(0, 1):
                self.app._screen.blit(self.sprites[self.__draw_counter +2], (int(self.pixel_pos.x), int(self.pixel_pos.y)))      
            elif self.direction == vec(-1, 0):
                self.app._screen.blit(self.sprites[self.__draw_counter +4], (int(self.pixel_pos.x), int(self.pixel_pos.y))) 
            elif self.direction == vec(0, -1):
                self.app._screen.blit(self.sprites[self.__draw_counter +6], (int(self.pixel_pos.x), int(self.pixel_pos.y)))
                
        else:
            if self.not_eaten:
                self.app._screen.blit(self.sprites[self.__draw_counter +8], (int(self.pixel_pos.x), int(self.pixel_pos.y)))  
            else:
                if self.direction == vec(1, 0):
                    self.app._screen.blit(self.sprites[10], (int(self.pixel_pos.x), int(self.pixel_pos.y)))          
                elif self.direction == vec(0, 1):
                    self.app._screen.blit(self.sprites[11], (int(self.pixel_pos.x), int(self.pixel_pos.y)))      
                elif self.direction == vec(-1, 0):
                    self.app._screen.blit(self.sprites[12], (int(self.pixel_pos.x), int(self.pixel_pos.y))) 
                elif self.direction == vec(0, -1):
                    self.app._screen.blit(self.sprites[13], (int(self.pixel_pos.x), int(self.pixel_pos.y)))
    
    
    def get_revesre_direction(self):
        
        if self.direction == vec(1,  0): return vec(-1, 0)
        if self.direction == vec(0,  1): return vec(0, -1)
        if self.direction == vec(-1, 0): return vec(1,  0)
        if self.direction == vec(0, -1): return vec(0,  1)
        
        
    def reset(self):
         
        self.grid_pos.x = self._initial_grid_pos.x
        self.grid_pos.y = self._initial_grid_pos.y
        self.direction = vec(0, -1)
        self.pixel_pos = self.get_pix_pos()
        self.leave_castle = False
    
    
    # palauttaa haamun ruutusijainnin perusteella keskitetyn pixeli sijainnin
    def get_pix_pos(self):
        return vec(self.grid_pos.x * self.app._cell_width  + TOP_BOTTOM_BUFFER//2,
                   self.grid_pos.y * self.app._cell_height + TOP_BOTTOM_BUFFER//2)
        

