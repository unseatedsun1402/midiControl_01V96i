from Connection import Connection
from Parser import Parser
from inputChannel import inputChannel
from AUXchannel import auxChannel
from BUSchannel import busChannel
from stereoBus import stereoBus
import VU
from errno import errorcode
import pygame as pg
from pygame.locals import *
import sys,pyaudio,time
import pygame.midi as midi
import threading
import gui
from gui import *


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
        
        global input
        global aux
        global bus
        global stereo
        global fadermode

        modes = {
            0:[0x7F,0x01,0x1C,0x00],
            1:[0x7F,0x01,0x23,0x02],
            2:[0x7F,0x01,0x23,0x05],
            3:[0x7F,0x01,0x23,0x08],
            4:[0x7F,0x01,0x23,0xb],
            5:[0x7F,0x01,0x23,0xe],
            6:[0x7F,0x01,0x23,0x11],
            7:[0x7F,0x01,0x23,0x14],
            8:[0x7F,0x01,0x23,0x17]
        }

        PARSER = Parser(connection)
        input =  {i:inputChannel(i,conn = connection,AUXCOUNT = 8, BusCOUNT=8) for i in range(32)}
        aux = {i:auxChannel(i,conn = connection) for i in range(8)}
        bus = {i:busChannel(i,conn = connection) for i in range(8)}
        stereo = stereoBus(conn = connection)

        fadermode = 0
        line = 1
        for each in input:
            if(input[each].id>15):
                    line = 0
            pos = ((input[each].id%16 * 30)+3,int((SCREENHEIGHT-(line*200))-30))
            input[each].on = onButton(x=pos[0],y=pos[1]-170,height =14, width =25)
            input[each].main = stereoButton(x=pos[0],y=pos[1]-185,height =14, width =25)
            input[each].fader = fader(x=pos[0],y=pos[1]-10,height =14, width = 15)

        stereo.fader = fader(x=680,y=295,height =20, width = 15,color = 'red',travel = 146)
        syncBtn = sync(x=400,y=20,height =15, width =35,onclickFunction=synConsole)
        for each in aux:
            aux[each].sendsonfaderBtn = Button(x=560+(30*(each%2)),y=180+((each//2)*25),height = 20, width = 25, buttonText=aux[each].short,onclickFunction=sendsonfader,val = each+1)
        mixView = Button(x=560,y=155,height = 20, width= 60, buttonText='mixView',onclickFunction=sendsonfader, val=0)
        #pass
        
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
                pos = ((input[each].id%16 * 30)+3,int((SCREENHEIGHT-(line*200))-30))
                input[each].draw(window,(pos[0],pos[1]+10))
                lbl = labelFont.render(input[each].short,True, (230,230,230))
                input[each].on.draw(window,input[each])
                input[each].main.draw(window,input[each])
                

                #draw/check current fader selection
                changes = input[each].fader.draw(window,input[each])
                if(changes[0]):
                    connection.output.write_sys_ex(when=midi.time(),msg=[0xF0,0x43,0x10,0x3E,modes[fadermode][0],modes[fadermode][1],modes[fadermode][2],modes[fadermode][3],each,0,0,input[each].faderlevel//128,input[each].faderlevel%128,0xF7])
                
                

                window.blit(lbl, (pos[0],pos[1]+2))

            #sends on fader
            mixView.draw(window)
            for each in aux:
                aux[each].sendsonfaderBtn.draw(window)
            

            #draw/check current fader selection
            changes = input[each].fader.draw(window,input[each])
            if changes[0]:
                connection.output.write_sys_ex(when=midi.time(),msg=[0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1C,0x00,each,0,0,input[each].faderlevel//128,input[each].faderlevel%128,0xF7])
                
            stereo.fader.draw(window,stereo)    

            '''changes = stereo.fader.draw(window,stereo)
            if changes[0]:
                stereo.send_fader() '''
            
            lbl = labelFont.render("Stereo LR",True, (230,230,230))
            
            stereo.draw(window,(720,320))
            
            syncBtn.draw(window)

            debug(window,input[1].faderlevel)

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
            pass
        else:
            skipped += 1
            if skipped > 100:
                pass
        
        update_meters()
        
        #check_changes()
        pg.display.update()
    
    while True:
        mainloop()

    

##--------Graphical user Interface-------##
SCREENWIDTH = 800
SCREENHEIGHT = 480

def find_01V96i_desk():
    '''finds the mixing desk in the midi interfaces'''
    midi.init()
    findA = b'Yamaha 01V96i Port1'
    input_id = -1
    output_id = -1

    nofdevices = midi.get_count()
    for i in range(nofdevices):
        device = midi.get_device_info(i)
        
        (interf, name, input, output, opened) = device
        name += b'_' # padding to ensure 'in' operation evalate to true if term == target
        if findA in name:
            if input == 1:
                input_id = i
            if output == 1:
                output_id = i
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

def check_changes(res):
    for each in res:
        match each[1]:

            case [0x7F,0x01,0x1c,0x00]:
                if (fadermode == 0):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].mainLR = (128*each[2][3])+each[3][0]
            #print(str('input '+str(each[2][0])+' fader = '+str(input[each[2][0]].faderlevel)))
            case [0x1a, 0x4, 0x5a, 0x0]:
                input[each[2][0]].mute = each[3][0]

            case [0x1a,0x3,0x2e,0x0]:
                input[each[2][0]].cue = each[3][0]

            case [0x7f,0x01,0x4f,0x00]:
                stereo.faderlevel = (128*each[2][3])+each[3][0]
            
            ## sends on aux mix
            case [0x7F,0x01,0x23,0x02]:         #AUX1
                if (fadermode == 1):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[0] = (128*each[2][3])+each[3][0]

            case [0x7F,0x01,0x23,0x05]:         #AUX2
                if (fadermode == 2):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[1] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0x08]:         #AUX3
                if (fadermode == 3):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[2] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0xb]:          #AUX4
                if (fadermode == 4):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[3] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0xe]:          #AUX5
                if (fadermode == 5):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[4] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0x11]:         #AUX6
                if (fadermode == 6):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[5] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0x14]:         #AUX7
                if (fadermode == 7):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[6] = (128*each[2][3])+each[3][0]
            
            case [0x7F,0x01,0x23,0x17]:         #AUX8
                if (fadermode == 8):
                    input[each[2][0]].faderlevel = (128*each[2][3])+each[3][0]
                input[each[2][0]].auxes[7] = (128*each[2][3])+each[3][0]

            case default:
                print([[hex(bit)for bit in bite] for bite in each])
            
            

def update_meters():
    try:
        updates = PARSER.listen()
        inp,bus,aux,st,resolution = updates
        for each in inp:
            input[each[0]].update_level(each[1])
        for each in st:
            stereo.update_level(each)
        if len(resolution) > 0:
            check_changes(resolution)
        #    print(resolution)
    except Exception as e:
        print(e)
    
    #time.sleep(1/15)

def synConsole():
    print('syncing...')
    for each in input:
        input[each].get_fader()
        input[each].get_auxes()
        #print(PARSER.listenFor(connection,[0xF0,0x43,0x10,0x3E],[0x7F,0x01,0x1C,0x00],each))
    print('synced')

def sendsonfader(mix):
    global fadermode
    fadermode = mix
    if mix == 0:
        for each in input:
            input[each].faderlevel = input[each].mainLR
    else:
        for each in input:
            input[each].faderlevel = input[each].auxes[mix-1]

    


test = [0xF0,0x43,0x30,0x3e,0x1a,0x00,0x00,0x00,0x12,0x00,0xf7]
prmChg = [0xF0,0x43,0x10,0x3e,0x1a]

if __name__ == '__main__':
    main()