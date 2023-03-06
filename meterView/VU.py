import pygame

class Meter():
    def draw(context: pygame.surface,level: int):
        """draws a meter for given input"""
        for i in range (level):
            if i < 20: 
                pygame.draw.rect(context (0, 192, 0), (10, (475-i*12), 30, 10))
            elif i >= 20 and i < 30:
                pygame.draw.rect(context, (255, 255, 0), (10, (475-i*12), 30, 10))
            else:
                pygame.draw.rect(context, (255, 0, 0), (10, (475-i*12), 30, 10))