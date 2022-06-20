'''
Created on 23 Jan 2020

@author: rasmus
'''




import  pygame
from    settings import BLACK




class Sprite_parser():
    
    def __init__(self, app):
        self.app = app
    
    
    
    def get_all_sprites(self, sheet):       
        sprite_Dict = {}
        
        sprite_Dict.update({"red_ghost": self.red_ghost(sheet)})
        
        sprite_Dict.update({"blue_ghost": self.blue_ghost(sheet)})
    
        sprite_Dict.update({"pink_ghost": self.pink_ghost(sheet)})
        
        sprite_Dict.update({"orange_ghost": self.orange_ghost(sheet)})
        
        sprite_Dict.update({"player": self.player(sheet)})
        
        return sprite_Dict
    
    
    def red_ghost(self, sheet):
            
        list = []
        for i in range(8):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (650, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        return self.vulnerable_ghost(sheet, list)
    
    
    def pink_ghost(self, sheet):
            
        list = []
        for i in range(8):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (700, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        return self.vulnerable_ghost(sheet, list)
    
    
    def blue_ghost(self, sheet):
            
        list = []
        for i in range(8):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (750, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        return self.vulnerable_ghost(sheet, list)
    
    
    def orange_ghost(self, sheet):
            
        list = []
        for i in range(8):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (800, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        return self.vulnerable_ghost(sheet, list)
    
    
    def vulnerable_ghost(self, sheet, list):
        
        for i in range(2):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (0, 50*i + 600, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        for i in range(5):
            
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (300, 50*i + 250, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
                    
        return list
    
    
    def player_death(self, sheet, list):
        
        for i in range(13):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (350, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
            
        return list
        
        
    def player(self, sheet):
            
        list = []
        for i in range(12):
        
            image = pygame.Surface([50, 50]).convert()
            
            image.blit(sheet, (0, 0), (850, 50*i, 50, 50))
            
            image = pygame.transform.scale(image, (self.app._cell_width + 8, self.app._cell_height + 8))
            
            image.set_colorkey(BLACK)
            
            list.append(image)
        
        return self.player_death(sheet, list)
        
        