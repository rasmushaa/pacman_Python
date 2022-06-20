'''
Created on 14 Jan 2020

@author: rasmus
'''




import  pygame
from    settings import *


vec = pygame.math.Vector2


''' pelaaja-olio alustettan aina app:ia luodessa
    eika pelia voi aloittaa ilman sita.
    pelaajan paikan voi kuitenikn maarittaa
    mazeLocations_filesta merkkkaamalla: "X"'''
class Player:
    
    def __init__(self, app, grid_pos):
    
        self.app                = app    
        self._initial_grid_pos  = vec(grid_pos.x ,grid_pos.y)
        self.__old_grid_pos     = vec(0, 0) 
        self.grid_pos           = grid_pos  
        self.__old_pix_pos      = vec(0, 0)
        self.pixel_pos          = self.get_pix_pos() 
        self.input_direction    = vec(1, 0)
        self.direction          = vec(1, 0)
        self.__able_to_move     = True
        self.current_score      = 0
        self.lives              = PLAYER_LIVES
        self.can_eat_ghost      = False
        self.__sprites          = self.app._sprites["player"]
        self.__draw_counter     = 0
        
        
        
    def update(self):
        
        # Jos hahmo on solun keskella, lue uusi suunta ja katso onko se mahdollinen
        if self.on_the_center():
            if self.can_move(self.input_direction, self.grid_pos):
                self.direction = self.input_direction
            self.__able_to_move = self.can_move(self.direction, self.grid_pos)
            
        # Jos kyseiseen suuntaan voi liikkua, liiku
        if self.__able_to_move:         
            self.pixel_pos += self.direction * PLAYER_SPEED  
            
            # Paivitaa animoinnissa kaytetyn: draw_countterin
            if abs(self.__old_pix_pos.x - self.pixel_pos.x) > self.app._cell_width*0.7 or abs(self.__old_pix_pos.y - self.pixel_pos.y) > self.app._cell_height*0.7:
                self.__old_pix_pos = self.get_pix_pos()
                self.__draw_counter += 1
                if self.__draw_counter > 2:
                    self.__draw_counter = 0
            
            
        # Paivittaa solun sijainnin
        self.grid_pos.x = (self.pixel_pos.x - TOP_BOTTOM_BUFFER + self.app._cell_width//2)   // self.app._cell_width + 1
        self.grid_pos.y = (self.pixel_pos.y - TOP_BOTTOM_BUFFER + self.app._cell_height//2) // self.app._cell_height + 1
        
        self.eat_item()
        
        
    def eat_item(self):
        if self.grid_pos in self.app.coins:
            if self.on_the_center():
                self.app.coins.remove(self.grid_pos)
                self.current_score += SCORE_COIN          
                if not self.app._sound_chanel.get_busy():
                    chanel = self.app._sound_chanel
                    chanel.play(self.app._sounds["eat"])
                    
        if self.grid_pos in self.app.power_coins:
            if self.on_the_center():
                self.app.power_coins.remove(self.grid_pos)
                self.current_score += SCORE_POWERUP          
                pygame.mixer.stop()
                self.app._sounds["power"].play()
                self.can_eat_ghost = True
        
    
    # Hahmon piirto riippuu sen suunnasta ja juoksevasta draw_counter laskurista
    def draw(self):       

        if self.direction == vec(1, 0):
            self.app._screen.blit(self.__sprites[self.__draw_counter], (self.pixel_pos.x, self.pixel_pos.y))             
        elif self.direction == vec(0, 1):
            self.app._screen.blit(self.__sprites[self.__draw_counter +3], (self.pixel_pos.x, self.pixel_pos.y))             
        elif self.direction == vec(-1, 0):
            self.app._screen.blit(self.__sprites[self.__draw_counter +6], (self.pixel_pos.x, self.pixel_pos.y))              
        elif self.direction == vec(0, -1):
            self.app._screen.blit(self.__sprites[self.__draw_counter +9], (self.pixel_pos.x, self.pixel_pos.y))    
            
            
    def draw_death(self):    
        for i in range(13):
            pygame.time.delay(50)
            pygame.draw.circle(self.app._screen, BLACK, (self.pixel_pos.x + self.app._cell_width//2, self.pixel_pos.y + self.app._cell_height//2), self.app._cell_width//2 + 5)
            self.app._screen.blit(self.__sprites[i + 10], (self.pixel_pos.x, self.pixel_pos.y))  
            pygame.display.update()
        
        
    def draw_lives(self):
        for i in range(self.lives):
            pygame.draw.circle(self.app._screen, PLAYER_COLOR, (TOP_BOTTOM_BUFFER//2 + 15 + i*25, TOP_BOTTOM_BUFFER//2 + MAZE_HEIGHT + 13), 10)
        
                
        
    # Keskikohta luetaan erikseen x- ja y-suunnalle. Alueella on cell/10 pixelin pelivara, jota käytetään vain, jos ruudun paikka on muuttunut
    def on_the_center(self):
        if int(self.pixel_pos.x - TOP_BOTTOM_BUFFER//2) % self.app._cell_width < self.app._cell_width//6:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                if self.grid_pos != self.__old_grid_pos:
                    self.__old_grid_pos.x = self.grid_pos.x
                    self.__old_grid_pos.y = self.grid_pos.y         
                    self.pixel_pos = self.get_pix_pos()
                return True
            
        if int(self.pixel_pos.y - TOP_BOTTOM_BUFFER//2) % self.app._cell_height < self.app._cell_height//6:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                if self.grid_pos != self.__old_grid_pos:
                    self.__old_grid_pos.x = self.grid_pos.x
                    self.__old_grid_pos.y = self.grid_pos.y
                    self.pixel_pos = self.get_pix_pos()
                return True
                
                
    def can_move(self, direction, grid_pos):
        for wall in self.app._walls:
            if direction + grid_pos == wall:
                return False
        return True
    
    
    def reset(self):
        
        self.grid_pos.x = self._initial_grid_pos.x
        self.grid_pos.y = self._initial_grid_pos.y
        self.pixel_pos = self.get_pix_pos()     
        self.direction = vec(1, 0)
        self.input_direction = vec(1, 0)
    
    
    def get_pix_pos(self):
        return vec(self.grid_pos.x * self.app._cell_width  + TOP_BOTTOM_BUFFER//2,
                   self.grid_pos.y * self.app._cell_height + TOP_BOTTOM_BUFFER//2)
        
        