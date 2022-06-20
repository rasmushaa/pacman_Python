'''
Created on 17 Jan 2020

@author: rasmus
'''




import  pygame,     heapq
from    settings    import *
from    heapq       import heappop

vec = pygame.math.Vector2



class Cell():

    def __init__(self, parent=None, position=None):
        
        self.parent = parent
        self.pos    = position
        self.dir    = vec(1, 0)
        self.g      = 0
        self.h      = 0
        self.f      = 0
        
    def __eq__(self, other):
        return self.pos == other.pos
    
    def __lt__(self, other):
        if self.f < other.f:
            return self
        else:
            return other


class A_star():
    
    def __init__(self):
        self.app = self.app
         
    def get_direction_to_target(self, target, start, restrict_reverse=False):
        
        DELAY = 80
        
        if target in self.app._walls:
            distance = 0
            while distance >= 0:
                distance += 1
                for direction in ALL_DIRECTION:    
                    
                    if ASTAR_VISUAL:
                        self.app.draw_cell(PLAYER_COLOR, target.x, target.y)
                        self.app.draw_cell((100, 100, 100), target.x + direction.x * distance, target.y + direction.y * distance)
                        pygame.display.update()
                        pygame.time.wait(100)
                    
                    if target + direction * distance not in self.app._walls:
                        if target.x + direction.x * distance < 28 and target.y + direction.y * distance < 30:
                            if target.x + direction.x * distance > 0 and target.y + direction.y * distance > 0:
                                target = target + direction * distance
                                if ASTAR_VISUAL: self.app.draw_cell(PLAYER_COLOR, target.x, target.y)
                                distance = -1
                                break
        
        start_cell  = Cell(None, start)
        target_cell = Cell(None, target)
               
        start_cell.g    = start_cell.h  = start_cell.f  = 0
        target_cell.g   = target_cell.h = target_cell.f = 0

        visited_list = []
        open_heap    = []
        
        

        heapq.heappush(open_heap, (start_cell.f, start_cell))
        
        while len(open_heap) > 0:
    
            temp_current_cell = heapq.heappop(open_heap)           
            current_cell = temp_current_cell[1]

            visited_list.append(current_cell)

            
            if ASTAR_VISUAL: 
                self.app.draw_cell((255, 0, 0), current_cell.pos.x, current_cell.pos.y)
                pygame.display.update()
                pygame.time.wait(DELAY)
            
            
            if current_cell == target_cell:
                while current_cell != start_cell:    
                    if ASTAR_VISUAL:   
                        for heap_cell in open_heap:
                            self.app.draw_cell((0, 255, 0), current_cell.pos.x, current_cell.pos.y)
                            pygame.display.update()                                            
                    if current_cell.parent == start_cell:
                        return current_cell.dir
        
                    current_cell = current_cell.parent              
                return vec(0, 0)
                
                      
            children = []
            for new_dir in POSSIBLE_DIRECTIONS:
                
                new_cell_pos = new_dir + current_cell.pos
                    
                if new_cell_pos in self.app._walls:               
                    continue
                
                if restrict_reverse and current_cell.pos == start:
                    if new_dir == self.get_revesre_direction():
                        continue
                
                new_cell = Cell(current_cell, new_cell_pos)
                
                new_cell.dir = new_dir
                
                children.append(new_cell)
                

            for child in children:
                if child in visited_list:
                    continue
                    
                child.g = abs(child.pos.x - current_cell.pos.x) + abs(child.pos.y - current_cell.pos.y)
                child.f = abs(child.pos.x - target.x) + abs(child.pos.y - target.y)
                child.h  = child.g + child.h
                    
                for heap_cell in open_heap:
                    cell_g = heap_cell[1].g
                    if child.g >= cell_g:
                        continue
                                    
                heapq.heappush(open_heap, (child.f, child))

            if ASTAR_VISUAL:   
                for heap_cell in open_heap:
                    self.app.draw_cell((255, 255, 100), heap_cell[1].pos.x, heap_cell[1].pos.y)
                    pygame.display.update()
                    pygame.time.wait(DELAY)
                
                
                    

                    

                    

                    


                
        
        