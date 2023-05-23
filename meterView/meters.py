from Connection import Connection
from Parser import Parser
from inputChannel import inputChannel
from stereoBus import stereoBus
import VU
from errno import errorcode
import pygame as pg
from pygame.locals import *
import sys,pyaudio,time
import pygame.midi as midi
import threading
import gui
from gui import onButton,stereoButton, fader


##--------Starting Variables-------##
connection = Connection
PARSER = Parser
frame = 0
skipped = 0
refreshTime = time.time()


def main():
    flags = pg.OPENGL
    pg.mixer.quit()
    pg.display.init()
    pg.font.init()
    font = pg.font.Font('freesansbold.ttf',18)
    window = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pg.display.set_caption('01v96i Control')
    pa = pyaudio.PyAudio()
    
    

    #info = pa.get_default_input_device_info()
    #RATE = int(info['defaultSampleRate'])


    try:
        device = find_01V96i_desk()
        connection = Connection(device)
        global PARSER
        PARSER = Parser(connection)
        global input
        input =  {i:inputChannel(i,conn = connection) for i in range(32)}
        global stereo
        stereo = stereoBus(conn = connection)
        line = 1
        for each in input:
            if(input[each].id>15):
                    line = 0
            pos = ((input[each].id%16 * 30)+3,int((SCREENHEIGHT-(line*180))-30))
            input[each].on = onButton(x=pos[0],y=pos[1]+15,height =14, width =25)
            input[each].main = stereoButton(x=pos[0],y=pos[1]-150,height =14, width =25)
            input[each].fader = fader(x=pos[0],y=pos[1]-20,height =14, width = 15)
        poll_meters()
            
    except:
        print("Connection failed")

    
    def draw():
        try:
            labelFont = pg.font.Font('freesansbold.ttf',11)
            line = 1
            for each in input:
                if(input[each].id>15):
                    line = 0
                pos = ((input[each].id%16 * 30)+3,int((SCREENHEIGHT-(line*180))-30))
                input[each].draw(window,(pos[0],pos[1]-10))
                lbl = labelFont.render(input[each].short,True, (230,230,230))
                input[each].on.draw(window,input[each])
                input[each].main.draw(window,input[each])
                input[each].fader.draw(window,input[each])
                window.blit(lbl, (pos[0],pos[1]+2))
            
            lbl = labelFont.render("Stereo LR",True, (230,230,230))
            stereo.draw(window,(720,320))
            window.blit(lbl, (700,330))

        except Exception as e:
            print(e)
            msg = pg.font.SysFont(None,24)
            error = msg.render("No Inputs",True,(230,50,10))
            rect = error.get_rect()
            window.blit(error,(int(SCREENWIDTH/2)-rect.centerx,int(SCREENHEIGHT/2)))
        
        
            
        
    def mainloop():
        global frame
        global skipped
        global refreshTime

        frametime = time.time()
        if (frametime - refreshTime > 10): #After 10 seconds meter polling stops sending values. needs to be called again
            poll_meters() #polls input meters
            refreshTime = time.time()
        
        if (frame < 15):
            frame += 1
        else: frame = 0

        window.fill((71,75,80))
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
                
        draw()
        #PARSER.listen()
        #print("frametime: " + str(time.time()-frametime))
        if time.time()-frametime > 0.010:
            update_meters()
        else:
            skipped += 1
            if skipped > 100:
                update_meters()
        
        
        pg.display.update()
    
    while True:
        mainloop()

    

##--------Graphical user Interface-------##
SCREENWIDTH = 800
SCREENHEIGHT = 480

def find_01V96i_desk():
    '''finds the mixing desk in the midi interfaces'''
    midi.init()
    findA = b'Yamaha 01V96i-1'
    input_id = -1
    output_id = -1
    for i in range(midi.get_count()):
        device = midi.get_device_info(i)
        
        (interf, name, input, output, opened) = device
        if findA in name:
            if input == 1:
                input_id = i
            if output == 1:
                output_id = i
        else:
            print(interf)
    midi.quit
    device = (input_id,output_id)
    return(device)

def poll_meters():
    for each in input:
        try:
            input[each].get_status()
        except Exception as e:
            print(e)
    stereo.get_status()

def update_meters():
    try:
        updates = PARSER.update_meters()
        inp,bus,aux,st = updates
        for each in inp:
            input[each[0]].update_level(each[1])
        for each in st:
            stereo.update_level(each)
    except Exception as e:
        print(e)
    
    #time.sleep(1/15)



test = [0xF0,0x43,0x30,0x3e,0x1a,0x00,0x00,0x00,0x12,0x00,0xf7]
prmChg = [0xF0,0x43,0x10,0x3e,0x1a]

if __name__ == '__main__':
    main()