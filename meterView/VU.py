import pygame

class Meter():
    def __init_(self):
        self.level = 0
    
    def update_level(self,data):
        self.level = ((4096*data[0])+(256*data[1])+(16*data[2])+data[3])
        return True
    
    def draw(self,context):
        """draws a meter for given input"""
        for i in range (0,self.level, 6):
            if i < 20: 
                pygame.draw.rect(context (0, 192, 0), (self.id*10, (475-i*6), 10, 5))
            elif i >= 20 and i < 30:
                pygame.draw.rect(context, (255, 255, 0), (self.id*10, (475-i*6), 10, 5))
            else:
                pygame.draw.rect(context, (255, 0, 0), (self.id*10, (475-i*6), 10, 5))