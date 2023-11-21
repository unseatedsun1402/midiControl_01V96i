"""Ui Elements for midiControl"""
import pygame
from pygame import font
from inputChannel import inputChannel
import math

global channel

class UIException(Exception):
    def __init__(self, *args):
         self.message = "UI error: "+ str(args)
         #return self.message

class sync():
    """Sync Element"""
    def __init__(self, x, y, width, height, buttonText='SYNC', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)

        self.fillColors = {
            'normal': '#CCAA22',
            'hover': '#ffff44',
            'pressed': '#77EE77',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+3,self.y+2,self.width,self.height)
        self.buttonSurf = labelFont.render(buttonText, True, (20, 20, 20))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))
    
    def draw(self,window):
        pos = pygame.mouse.get_pos()
            
        if self.buttonRect.collidepoint(pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onclickFunction()    
                
        else:
            self.buttonSurface.fill(self.fillColors['normal'])
        
        window.blit(self.buttonSurface,self.buttonRect)
        window.blit(self.buttonSurf,self.textRect)
        #window.blit(self.indicatorSurf,self.indicator)

class Button():
    """Misc Element"""
    def __init__(self, x, y, width, height, buttonText=None, onclickFunction=None, onePress=False, val =None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.val = val
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)

        self.fillColors = {
            'normal': '#AA22CC',
            'hover': '#BB22BB',
            'pressed': '#dddddd',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+3,self.y+2,self.width,self.height)
        self.buttonSurf = labelFont.render(buttonText, True, (20, 20, 20))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))
    
    def draw(self,window):
        pos = pygame.mouse.get_pos()
            
        if self.buttonRect.collidepoint(pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onclickFunction(self.val)    
                
        else:
            self.buttonSurface.fill(self.fillColors['normal'])
        
        window.blit(self.buttonSurface,self.buttonRect)
        window.blit(self.buttonSurf,self.textRect)
        #window.blit(self.indicatorSurf,self.indicator)

class knob():
    def __init__(self,x,y,radius,label,colour,onclickFuntion=None,onePress=False):
        self.x = x
        self.y = y
        self.width = radius
        self.height = radius
        self.clicked = False
        labelFont = font.Font('freesansbold.ttf',11)

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.textRect = pygame.Rect(self.x+3,self.y,self.width,self.height)
        self.buttonSurf = labelFont.render(label, True, (20, 20, 20))
        self.indicator = pygame.Rect(self.x+6,self.y+10,self.width/2,self.height/5)
        self.indicatorSurf = pygame.Surface((self.width/2, self.height/5))

    def draw(self,window,**kwargs):
        pos = pygame.mouse.get_pos()
        channel = kwargs['channel']
        control = kwargs['control']
        if channel.auxOn[control]:
            pass
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
    def __init__(self,**kwargs,):
        try:
            if 'color' in kwargs:
                match kwargs['color']:
                    case 'red':
                        self.colour = (230,10,10)
                    case 'blue':
                        self.colour = (10,10,230)
                    case 'yellow':
                        self.colour = (230,230,10)
            else:
                self.colour = (44,44,44)
            self.highlight = (196,196,196)
            self.x = kwargs['x']
            self.y =  kwargs['y']
            self.position = 0
            self.width =  kwargs['width']
            self.height =  kwargs['height']
            if 'travel' in kwargs:
                self.travel = 147
            else:
                self.travel = 147
            self.dragged = 0
            self.clicked = False
            
            self.travelSurface = pygame.Surface((self.width, self.height))
            self.buttonRect = pygame.Rect(self.x, self.y+self.position, self.width, self.height)
            self.travelSurface.fill(self.colour)
        
        except:
            raise UIException('color not found')
    
    def draw(self,window,channel):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        collides = self.buttonRect.collidepoint(pos)
        change = False
        self.position = channel.faderlevel//7

        if collides:
            self.travelSurface.fill((self.highlight))

        else:
            self.travelSurface.fill((self.colour))
        
        if pressed:
            if collides:
                if not self.clicked:
                    self.dragged = pos[1]
                    self.clicked = True
                    #print('clicked: ' + str(self.dragged))
            
            ## checks position of mouse and moves fader
            if self.clicked:
                change = True
                distancemoved =  self.dragged-pos[1]
                #print('distance moved: ' + str(distancemoved))

                if(distancemoved < self.travel):
                    if (self.position + distancemoved > self.travel):
                        self.position = self.travel

                    elif(self.position + distancemoved <= 0):
                        self.position = 0
                    
                    else:
                        self.position += distancemoved
                

                self.dragged = pos[1] #reset dragged value after finding new fader position

                channel.set_fader(abs(self.position)*7)
        else:
            if self.clicked:
                self.clicked = False
                #print('released ' + str(channel.id))

        self.buttonRect = pygame.Rect(self.x, self.y-self.position, self.width, self.height)
        window.blit(self.travelSurface,self.buttonRect)
        return (change,self.position)


def debug(window,content):
    font = pygame.font.Font('freesansbold.ttf',18)
    information = font.render(str(content),True,(240,240,24))
    informationSurface = pygame.Rect(600,300,50, 50)
    window.blit(information, informationSurface)
    return