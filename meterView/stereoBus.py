"""Yamaha digital mixer virtual input channel object"""
import Connection, VU
import time
import pygame.midi as midi
import pygame

sysExChg = [0xF0,0x43,0x10,0x3E]
sysExReq = [0xf0,0x43,0x30,0x3e]

class stereoBus():
    """Yamaha digital mixer virtual stereo bus object"""
    connection = Connection

    def __init__(self,conn: Connection):
        """Pass connection"""
        self.connection = conn
        self.id = 0x4D
        self.levelL = 0
        self.levelR = 0
        self.fader = object
        
        self.faderlevel = -1


    def get_status(self):
        """polls meter value meter value data"""
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x30,0x3E,0x1A,0x21,0x04,0x00,0x7f,0x00,0x01,0xf7],when=midi.time())

    def update_level(self,data):
        self.levelL = (data[0])
        self.levelR = (data[1])
        return True
    
    def get_fader(self):
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x30,0x3E,0x7f,0x01,0x4f,0x00,0x00,0xf7],when=midi.time())

    def set_fader(self,data):
        self.faderlevel = data
    
    def send_fader(self):
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7f,0x01,0x4f,0x0,0x00,0x00,(self.faderlevel//128),(self.faderlevel%128),0xf7],when=midi.time())

    def draw(self,context,pos):
        """draws a meter for given input"""
        
        segment = 0
        for i in range (884,self.levelL, 64):
            if (i>4096):
                break
            segment += 1
            if i < 3000: 
                pygame.draw.rect(context, (0, 192, 0), (pos[0]-7,pos[1]-(segment*5)-2, 10, 5))
            elif i >= 3000 and i < 4000:
                pygame.draw.rect(context, (255, 200, 0), (pos[0]-7, pos[1]-(segment*5)-2, 10, 5))
            else:
                pygame.draw.rect(context, (255, 0, 0), (pos[0]-7, pos[1]-(segment*5)-2, 10, 5))

        segment = 0
        for i in range (884,self.levelR, 64):
            if (i>4096):
                break
            segment += 1
            if i < 3000: 
                pygame.draw.rect(context, (0, 192, 0), (pos[0]+7,pos[1]-(segment*5)-2, 10, 5))
            elif i >= 3000 and i < 4000:
                pygame.draw.rect(context, (255, 200, 0), (pos[0]+7, pos[1]-(segment*5)-2, 10, 5))
            else:
                pygame.draw.rect(context, (255, 0, 0), (pos[0]+7, pos[1]-(segment*5)-2, 10, 5))