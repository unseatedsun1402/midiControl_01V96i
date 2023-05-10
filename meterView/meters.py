from Connection import Connection
from Parser import Parser
from  inputChannel import inputChannel
import VU
from errno import errorcode
import pygame as pg
from pygame.locals import *
import sys,pyaudio,wave,audioop,math,time
import pygame.midi as midi
import threading


##--------Starting Variables-------##
connection = Connection
PARSER = Parser
frame = 0


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
        input =  {i:inputChannel(i,conn = connection) for i in range(40)}
            
    except:
        print("Connection failed")

    
    def draw():
        try:
            for each in input:
                pos = (input[each].id * 10,(SCREENHEIGHT/2)-18)
                input[each].meter.draw(window)
                lbl = font.render(text = input[each].short,antialias = True, color = ((230,230,230)))
                window.blit(lbl, (pos[0],pos[1]))

                pg.draw.rect(window,color=(140,110,80),rect=(pos,(10,10)))
        except Exception as e:
            print(e)
            msg = pg.font.SysFont(None,24)
            error = msg.render("No Inputs",True,(230,50,10))
            rect = error.get_rect()
            window.blit(error,(int(SCREENWIDTH/2)-rect.centerx,int(SCREENHEIGHT/2)))
        
        
            
        
    def mainloop():
        frametime = time.time()
        window.fill((71,75,80))
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
        
        update_meters()
        draw()
        
        global frame
        if frame <= 100:
            frame += 1
        else:
            time.sleep(0.5)
            frame = 0
        time.sleep(0.0012)
        pg.display.update()
    
    
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
    midi.quit
    device = (input_id,output_id)
    return(device)


def update_meters():
    for each in input:
        try:
            input[each].get_status()
        except Exception as e:
            print(e)
    try:
        updates = PARSER.update_meters()
        inp,bus,aux,st = updates
    except Exception as e:
        print(e)
    for each in inp:
        input[each[0]].update_level(each[1])
    #time.sleep(1/15)



test = [0xF0,0x43,0x30,0x3e,0x1a,0x00,0x00,0x00,0x12,0x00,0xf7]
prmChg = [0xF0,0x43,0x10,0x3e,0x1a]

if __name__ == '__main__':
    main()