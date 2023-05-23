"""Ui Elements for midiControl"""
import pygame
from pygame import font
from inputChannel import inputChannel

class onButton(inputChannel):
    """Mute UI Element"""
    def __init__(self, x, y, width, height, buttonText='ON', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)
        self.mute = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+3,self.y,self.width,self.height)
        self.buttonSurf = labelFont.render(buttonText, True, (20, 20, 20))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))
    
    def draw(self,window,channel):
        pos = pygame.mouse.get_pos()
        if(channel.mute == 1):
            self.indicatorSurf.fill((196,100,44))
        else:
            self.indicatorSurf.fill((44,44,44))
            

        if self.buttonRect.collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0]:
                if self.clicked:
                    pass
                else:
                    channel.inputOn()
                    self.clicked = True
                    
            else:
                self.clicked = False
            self.buttonSurface.fill((240,100,44))
        else:
            self.buttonSurface.fill((196,196,196))
        
        window.blit(self.buttonSurface,self.buttonRect)
        window.blit(self.buttonSurf,self.textRect)
        window.blit(self.indicatorSurf,self.indicator)

class stereoButton(inputChannel):
    """Stereo UI Element"""
    def __init__(self, x, y, width, height, buttonText='LR', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)
        self.mute = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+4,self.y,self.width,self.height)
        self.buttonSurf = labelFont.render(buttonText, True, (220,220,220))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))
    
    def draw(self,window,channel):
        pos = pygame.mouse.get_pos()
        if(channel.stereo == 1):
            self.indicatorSurf.fill((196,100,44))
        else:
            self.indicatorSurf.fill((44,44,44))
            

        if self.buttonRect.collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0]:
                if self.clicked:
                    pass
                else:
                    channel.stereoOn()
                    self.clicked = True
                    
            else:
                self.clicked = False
            self.buttonSurface.fill((240,160,160))
        else:
            self.buttonSurface.fill((240,120,120))
        
        window.blit(self.buttonSurface,self.buttonRect)
        window.blit(self.buttonSurf,self.textRect)
        window.blit(self.indicatorSurf,self.indicator)

class selectButton(inputChannel):
    """Select UI Element"""
    def __init__(self, x, y, width, height, buttonText='SEL', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)
        self.mute = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+3,self.y,self.width,self.height)
        self.buttonSurf = labelFont.render(buttonText, True, (20, 20, 20))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))
    
    def draw(self,window,channel):
        pos = pygame.mouse.get_pos()
        if(channel.selected == 1):
            self.indicatorSurf.fill((150,196,50))
        else:
            self.indicatorSurf.fill((44,44,44))
            

        if self.buttonRect.collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0]:
                if self.clicked:
                    pass
                else:
                    channel.select()
                    self.clicked = True
                    
            else:
                self.clicked = False
            self.buttonSurface.fill((240,100,44))
        else:
            self.buttonSurface.fill((196,196,196))
        
        window.blit(self.buttonSurface,self.buttonRect)
        window.blit(self.buttonSurf,self.textRect)
        window.blit(self.indicatorSurf,self.indicator)

class fader():
    """Fader UI Element"""
    def __init__(self,x,y,width,height):
        self.colour = (44,44,44)
        self.x = x
        self.y = y
        self.position = 0
        self.width = width
        self.height = height
        self.travel = 115
        self.dragged = 0
        self.clicked = False
        
        self.travelSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y+self.position, self.width, self.height)
        self.travelSurface.fill(self.colour)
    
    def draw(self,window,channel):
        pos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(pos):
            self.travelSurface.fill((196,196,196))
            if pygame.mouse.get_pressed()[0]:
                if self.clicked: 
                    pass
                else:
                    self.dragged = pygame.mouse.get_pos()[1]
                    self.clicked = True          
            else:
                self.clicked = False
                self.dragged = 0
        else:
            self.travelSurface.fill(self.colour)
        
        if self.clicked: #checks position of mouse and moves fader
            if pygame.mouse.get_pressed()[0]:
                moved = (self.dragged-pos[1])
                if(moved-self.position > 0):
                    if (moved-self.position<self.travel):
                        self.position = (self.position-moved)
                        self.buttonRect = pygame.Rect(self.x, self.y+self.position, self.width, self.height)
                    else:
                        self.position = self.travel
                else:
                    self.position = 0
            else:
                self.clicked = False
                self.dragged = 0
    
        window.blit(self.travelSurface,self.buttonRect)