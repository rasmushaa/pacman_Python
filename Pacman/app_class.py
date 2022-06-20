'''
Created on 14 Jan 2020

@author: rasmus
'''




import  pygame, sys, pickle
from    settings                    import *
from    player_class                import Player
from    blue_ghost_class            import Blue_ghost
from    red_ghost_class             import Red_ghost
from    orange_ghost_class          import Orange_ghost
from    pink_ghost_class            import Pink_ghost
from    items_class                 import Item
from    sprite_sheet_parser_class   import Sprite_parser



pygame.init()
pygame.font.init()
pygame.mixer.init()
vec = pygame.math.Vector2

 


class App:
    
    def __init__(self):
        
        self._screen            = pygame.display.set_mode((WIDTH, HEIGHT))
        self._sound_chanel      = pygame.mixer.Channel(1)
        self.__clock            = pygame.time.Clock()
        self._cell_width        = MAZE_WIDTH//CELL_X
        self._cell_height       = MAZE_HEIGHT//CELL_Y
        self.__running          = True
        self.__state            = "start"
        self.__time_from_start  = 0
        self.timer              = 0
        self._enemies           = []
        self._walls             = []
        self.__items            = []
        self.coins              = []
        self.power_coins        = []
        self._sounds            = {}
        self._sprites           = {} 
        self.__top_score        = 0
        self._level             = 1       
        self.load()  
        self._player            = Player(self, vec(1, 1)) 
            
    
    def run(self):
        while self.__running:
            if self.__state == "start":
                self.start_events()
                self.start_updates()
                self.start_draw()
                
            elif self.__state == "playing":
                pass
                self.playing_events()
                self.playing_updates()
                self.playing_draw()
                
            elif self.__state == "endgame":
                self.endgame_events()
                self.endgame_updates()
                self.endgame_draw()
                
            else:
                self.__running = False
            self.__clock.tick(FPS)
                       
        pygame.quit()
        sys.exit()
    
    
    
    
    ##################################### HELPER FUNCTIONS ##################################
    
    
    # Piirtaa teksitin parametrien perusteella. Centered laittaa sen keskelle locaatiota
    def draw_text(self, words, screen, location, size, color, fontName, centered=False):
        
        font = pygame.font.SysFont(fontName, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            location[0] = location[0] - text_size[0] // 2
            location[1] = location[1] - text_size[1] // 2
        screen.blit(text, location)
        pass
        
    
    def load(self):          
        try:
            # Lisaa hahmojen kuvat sprite-sanakirjaan
            Parser = Sprite_parser(self)         
            spriteSheet = pygame.image.load("pacManSpreetSheet.png")
            self._sprites = Parser.get_all_sprites(spriteSheet)
            
            # Lisaa aanet aani-sanakirjaan
            self._sounds.update({"eat":   (pygame.mixer.Sound("pacManEat.wav"))})
            self._sounds.update({"power": (pygame.mixer.Sound("pacManPower.wav"))})
            self._sounds.update({"ghost": (pygame.mixer.Sound("pacManGhost.wav"))})
            self._sounds.update({"intro": (pygame.mixer.Sound("pacManIntro.wav"))})
            self._sounds.update({"death": (pygame.mixer.Sound("pacManDeath.wav"))})
            
            # Asettaa taustakuvan oikean kokoiseksi
            self.background = pygame.image.load("mazePicture.png")  
            self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
            
            # Lukee high score pisteet save-tiedostosta
            from_save_file = open("pacManSaveFile.bin", "rb")
            self.__top_score = pickle.load(from_save_file)
            from_save_file.close() 
            
            # Katsoo mita asoita kartaan on merkitty ja lisaa ne peliin
            with open("mazeLocations.txt", "r") as file:
                for y_index, line in enumerate(file):
                    for x_index, char in enumerate(line):
                        
                        if char == "1":
                            self._walls.append(vec(x_index, y_index))                          
                        elif char == ".":
                            self.coins.append(vec(x_index, y_index))
                            self.__items.append(Item(self, vec(x_index, y_index), "coin"))                         
                        elif char == "+":
                            self.power_coins.append(vec(x_index, y_index))
                            self.__items.append(Item(self, vec(x_index, y_index), "powerUp"))                          
                        elif char == "X":
                            self._player = Player(self, vec(x_index, y_index))                          
                        elif char == "B":
                            self._enemies.append(Blue_ghost(self, vec(x_index, y_index)))  
                        elif char == "R":                            
                            self._enemies.append(Red_ghost(self, vec(x_index, y_index)))                          
                        elif char == "O":
                            self._enemies.append(Orange_ghost(self, vec(x_index, y_index)))                          
                        elif char == "P":
                            self._enemies.append(Pink_ghost(self, vec(x_index, y_index)))                           
                        elif char == "-":
                            pygame.draw.rect(self.background, BLACK, (x_index * self._cell_width,y_index * self._cell_height,                                 
                                                                      self._cell_width, self._cell_height))
                            
        except FileNotFoundError as file_error:
            print(file_error)
            print("\n\nProgram exits...?!?!\n\n")
            self.__running = False

                                  
                     
    def draw_grid(self):      
        for x in range(MAZE_WIDTH//self._cell_width):   
            pygame.draw.line(self.background, (100, 100, 100), (x * self._cell_width, 0), (x * self._cell_width, MAZE_HEIGHT))         
        for y in range(MAZE_HEIGHT//self._cell_height):          
            pygame.draw.line(self.background, (100, 100, 100), (0, y * self._cell_height), (MAZE_WIDTH, y * self._cell_height))
                  
        for wall in self._walls:
            self.draw_cell((10, 10, 130), wall.x, wall.y)
            
        self.draw_cell(WHITE, self._player.grid_pos.x, self._player.grid_pos.y, 1)      
        for enemy in self._enemies:
            self.draw_cell(enemy.color, enemy.grid_pos.x, enemy.grid_pos.y, 1)
            self.draw_cell(enemy.color, enemy.target.x, enemy.target.y, 2)

 
    def draw_cell(self, color, x0, y0, fill=0): 
        pygame.draw.rect(self._screen, color, (x0 * self._cell_width + TOP_BOTTOM_BUFFER//2,
                                              y0 * self._cell_height + TOP_BOTTOM_BUFFER//2,
                                              self._cell_width, self._cell_height), fill)  
        
        
    def draw_items(self):
        for coin in self.coins:
            pygame.draw.circle(self._screen, COIN_COLOR, (coin.x * self._cell_width + self._cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                                          coin.y * self._cell_height + self._cell_width//2+ TOP_BOTTOM_BUFFER//2), 
                                                          self._cell_width//6)  
        for powerUp in self.power_coins:
            pygame.draw.circle(self._screen, POWER_COLOR, (powerUp.x * self._cell_width + self._cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                                           powerUp.y * self._cell_height + self._cell_width//2+ TOP_BOTTOM_BUFFER//2), 
                                                           self._cell_width//3)  
                 
      
    def player_enemy_collade(self, pos1, pos2):
        if abs((pos1.x + self._cell_width//2) - (pos2.x + self._cell_width//2)) < self._cell_width:
            if abs((pos1.y + self._cell_height//2) - (pos2.y + self._cell_height//2)) < self._cell_height:
                return True
        return False
        
        
    def reduce_life(self):                
        pygame.time.delay(1300)
                
        self._player.reset()
        for ghost in self._enemies:
            ghost.reset()

        self.playing_draw()
        pygame.display.update()
        pygame.time.delay(2000)
        
        
    def add_level(self):
        self._level += 1
        
        # Keraa kolikot ja muut uudelleen kaytton Items-listasta
        for item in self.__items:
            if item.item_type == "coin":
                self.coins.append(item.grid_pos)
            elif item.item_type == "powerUp":
                self.power_coins.append(item.grid_pos)
                
        self.reduce_life()
        
    
    def reset_game(self):
        self._player.lives = PLAYER_LIVES
        self._player.current_score = 0      
        self.__state = "playing" 
        self._level = 0
        self.coins.clear()  
        self.power_coins.clear()  
        self.add_level()             
        
            
        
        
        
    ##################################### SART FUNCTIONS ####################################
      
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__state = "playing"
                               
                
    def start_updates(self):
        if self.__time_from_start == 0:
            self._sounds["intro"].play()
            self.__time_from_start = 1
    
    
    def start_draw(self):
        self._screen.fill(BLACK)
        
        self.draw_text("PUSH SPACE BAR",                            self._screen, [WIDTH//2, HEIGHT//2 - 50],    START_TEXT_SIZE, (170, 132, 58),    START_FONT, centered=True)
        self.draw_text("1 PLAYER ONLY",                             self._screen, [WIDTH//2, HEIGHT//2 + 50],    START_TEXT_SIZE, (44, 167, 198),    START_FONT, centered=True)
        self.draw_text("© 2020 RAZZE CO.",                          self._screen, [WIDTH//2, HEIGHT//2 + 150],   START_TEXT_SIZE, (250, 210, 240),   START_FONT, centered=True)
        self.draw_text("HIGH SCORE: {}".format(self.__top_score),   self._screen, [4, 0],                        START_TEXT_SIZE, (255, 255, 255),   START_FONT)
        
        pygame.display.update()
        
        
        
    ##################################### PLAYING FUNCTIONS #################################
      
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self._player.input_direction = vec(-1, 0)
                    
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self._player.input_direction = vec(1, 0)
                    
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self._player.input_direction = vec(0, -1)
                    
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self._player.input_direction = vec(0, 1)
                    
                
    def playing_updates(self):
        
        # Paivittaa kellon ja minuuttti taimerin
        self.timer = pygame.time.get_ticks() - self.__time_from_start
        if self.timer > 30000:
            self.__time_from_start = pygame.time.get_ticks()
            
        # Paivittaa pelaajan ,viholliset ja elamat
        self._player.update()    
        for enemy in self._enemies:      
             
            # jos pelaaja on syonyt voimapallon -> haamut pelkaavat
            if self._player.can_eat_ghost:
                enemy.state = "scared"    
             
            enemy.update()
            
            # jos pelaaja voi kuolla ja hamamut eivat pelkaa -> katso onko pelaaja kuollut
            if CAN_DIE and enemy.state != "scared":
                if self.player_enemy_collade(self._player.pixel_pos, enemy.pixel_pos):
                    self._player.lives -= 1
                    self._player.draw_death()
                    pygame.mixer.stop()
                    self._sounds["death"].play()
                    if self._player.lives <= 0:
                        pygame.time.delay(500)
                        self.__state = "endgame"
                    else:
                        self.reduce_life()
            
            # jos haamut pelokkaita -> katso onko haamu syoty          
            if enemy.state == "scared":
                if self.player_enemy_collade(self._player.pixel_pos, enemy.pixel_pos) and enemy.not_eaten:
                    pygame.mixer.stop()
                    self._sounds["ghost"].play()
                    self._player.current_score += SCORE_GHOST
                    enemy.not_eaten = False
        
        # resetoi pelaajan mahdollisuus syoda haamuja
        if self._player.can_eat_ghost:         
            self._player.can_eat_ghost = False
                                   
        # Jos kolikot ovat loppuneet, lisaa uusi leveli                  
        if len(self.coins) == 0:
            self.add_level()
          
        # Paivittaa huippupisteet jos tarvitsee    
        if self._player.current_score >= self.__top_score:
            self.__top_score = self._player.current_score
    
    
    def playing_draw(self):
        
        self._screen.fill(BLACK)
        self._screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
                
        # Jos gridi on kaytossa -> piirra se
        if GRID_ON: self.draw_grid()
        
        # Piirtaa pelin pistetilanteet
        self.draw_text("CURRENT SCORE: {}".format(self._player.current_score),   self._screen, [30,           1], 18, WHITE, START_FONT)
        self.draw_text("HIGH SCORE: {}".format(self.__top_score),                self._screen, [WIDTH//2 + 80,1], 18, WHITE, START_FONT)
        self.draw_text("{}".format(self._level),                                 self._screen, [WIDTH//2,     1], 20, WHITE, START_FONT)
        
        # Piirtaa kaikki hahmot ja itemit
        self.draw_items()  
        self._player.draw()
        self._player.draw_lives()
        for enemy in self._enemies:
            enemy.draw()
        
        pygame.display.update()
        
        
        
    ##################################### ENDGAME FUNCTIONS #################################
    
    def endgame_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                             
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._player.current_score = 1
                self.__top_score = 1
  
    
    def endgame_updates(self):
        
        if self._player.current_score >= self.__top_score:
            to_save_file = open("pacManSaveFile.bin", "wb")
            pickle.dump(self.__top_score, to_save_file)
            to_save_file.close() 
            
    
    
    def endgame_draw(self):
        self._screen.fill(BLACK)
        
        self.draw_text("GAME OVER!",                                        self._screen, [WIDTH//2, HEIGHT//2 -190],    26,              (170, 132, 58),    START_FONT, centered=True)
        self.draw_text("HIGH SCORE: {}".format(self.__top_score),           self._screen, [WIDTH//2, HEIGHT//2 - 150],   18,              (255, 255, 255),   START_FONT, centered=True)
        self.draw_text("YOUR SCORE: {}".format(self._player.current_score), self._screen, [WIDTH//2, HEIGHT//2 - 120],   17,              (255, 255, 255),   START_FONT, centered=True)
        self.draw_text("PUSH SPACE BAR TO PLAY AGAIN",                      self._screen, [WIDTH//2, HEIGHT//2 - 40],    START_TEXT_SIZE, (170, 132, 58),    START_FONT, centered=True) 
        self.draw_text("esc to quit",                                       self._screen, [WIDTH//2, HEIGHT//2 - 0],     12,              (255, 255, 255),   START_FONT, centered=True)
        self.draw_text("r to reset score",                                  self._screen, [WIDTH//2, HEIGHT//2 + 20],    12,              (255, 255, 255),   START_FONT, centered=True) 
        self.draw_text("© 2020 RAZZE CO.",                                  self._screen, [WIDTH//2, HEIGHT//2 + 160],   START_TEXT_SIZE, (250, 210, 240),   START_FONT, centered=True)                                                                    
        
        pygame.display.update()
        


