"""Yamaha digital mixer virtual input channel object"""
import Connection, VU
import time
import pygame.midi as midi
import pygame
from Parser import Parser,ResponseException

sysExChg = [0xF0,0x43,0x10,0x3E]
sysExReq = [0xF0,0x43,0x30,0x3E]
chanOn = [0x7F,0x01,0x1A,0x00]
toStereo = [0x7F,0x01,0x22,0x00]
chanPan = [0x7F,0x01,0x1A,0x00]
chanFad = [0x7F,0x01,0x1B,0x00]
chanAtt = [0x7F,0x01,0x1C,0x00]
select = [0x1A,0x04,0x09,0x18]

class inputChannel():
    """Yamaha digital mixer virtual input channel object"""
    connection = Connection

    def __init__(self,val: int,conn: Connection):
        """Pass an integer value to identify the channel"""
        self.connection = conn
        self.id = val
        self.level = 0
    
        self.on = object
        self.main = object
        self.fader = object

        self.mute = -1
        self.stereo = -1
        self.selected = -1
        
        try:
            if self.id<32:
                self.short = self.__get_short()
                #self.name = self.__get_name()
                self.getinputOn()
                self.getStereo()
            else:
                self.short = str("ST 41" + str(self.id % 32))
                self.name = str("STIN" + str(self.id % 32))
        except Exception as e: 
            print(e)
        
        
        self.meter = VU.Meter()
        
    
    def __get_short(self):
        """Gets short (xxxx) channel name"""
        msg = [0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
        msg.append(0xf7)
        message = ['1','2','3','4']
        i = 0
        while i <= 3:
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] = i
            time.sleep(0.001)
            sysex = []
            reading = False
            buffer = self.connection.input.read(256)
            for events in range(len(buffer)-1):
                try:
                    if not reading:
                        if set(sysExChg).issubset(buffer[events][0]):
                            #message[i] = events[0].append(list(each for each in events[0]))
                            reading = True
                            for each in buffer[events][0]:
                                sysex.append(each)
                    elif [0x1a,0x02,0x04,i] == buffer[events][0]:
                        for each in buffer[events][0]:
                            sysex.append(each)
                        if set([self.id,0x00,0x00]).issubset(buffer[events+1][0]):
                            message[i] = chr(buffer[events+2][0][0])
                            i += 1
                            reading = False
                            sysex = []
                    else:
                        reading = False
                        sysex = []
                except Exception as e:
                    print(e)
        name = ''
        for each in message:
            name = name + each
        return (name)

    def __get_name(self):
        """Gets long channel name"""
        msg = [0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x04,self.id]
        msg.append(0xf7)
        message = [str(each) for each in range(16)]
        i = 4
        while i < 20:
            self.connection.output.write_sys_ex(msg= msg,when= midi.time())
            msg[7] = i
            time.sleep(0.001)
            sysex = []
            reading = False
            buffer = self.connection.input.read(256)
            for events in range(len(buffer)-1):
                try:
                    if not reading:
                        if set(sysExChg).issubset(buffer[events][0]):
                            #message[i] = events[0].append(list(each for each in events[0]))
                            reading = True
                            for each in buffer[events][0]:
                                sysex.append(each)
                    elif [0x1a,0x02,0x04,i] == buffer[events][0]:
                        for each in buffer[events][0]:
                            sysex.append(each)
                        if set([self.id,0x00,0x00]).issubset(buffer[events+1][0]):
                            message[i-4] = chr(buffer[events+2][0][0])
                            i += 1
                            reading = False
                            sysex = []
                    else:
                        reading = False
                        sysex = []
                except Exception as e:
                    print(e)
        name = ''
        for each in message:
            name = name + each
        return (name)

    def get_status(self):
        """polls meter value meter value data"""
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x30,0x3E,0x1A,0x21,0x00,0x00,self.id,0x00,0x01,0xf7],when=midi.time())

    def update_level(self,data):
        self.level = (data)
        return True

    def getinputOn(self):
        message = [each for each in sysExReq]
        for each in chanOn:
            message.append(each)
        for each in [self.id,0xF7]:
            message.append(each)

        while (self.mute == -1):
            self.connection.output.write_sys_ex(msg = message,when=midi.time())
            time.sleep(0.005)
            try:
                self.mute = Parser.listenFor(self.connection,sysExChg,chanOn,self.id)[4]
            except ResponseException as e:
                pass
    

    def inputOn(self):
        if (self.mute == 0):
            self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1A,0x00,self.id,0x00,0x00,0x00,0x01,0xf7],when=midi.time())
            self.mute = 1
        else:
            self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x1A,0x00,self.id,0x00,0x00,0x00,0x00,0xf7],when=midi.time())
            self.mute = 0
    
    def getStereo(self):
        message = [each for each in sysExReq]
        for each in toStereo:
            message.append(each)
        for each in [self.id,0xF7]:
            message.append(each)

        while (self.stereo == -1):
            self.connection.output.write_sys_ex(msg = message,when=midi.time())
            time.sleep(0.005) #waiting for the mixer as searching for a response immediately often is does not allow enough time for the mixer to respond
            try:
                self.stereo = Parser.listenFor(self.connection,sysExChg,toStereo,self.id)[4]
            except ResponseException as e:
                pass

    def stereoOn(self):
        
        if (self.stereo == 0):
            self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x22,0x00,self.id,0x00,0x00,0x00,0x01,0xf7],when=midi.time())
            
            self.stereo = 1
        else:
            self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x22,0x00,self.id,0x00,0x00,0x00,0x00,0xf7],when=midi.time())
            self.stereo = 0
    
    def getSelect(self):
        message = [each for each in sysExReq]
        for each in select:
            message.append(each)
        for each in [self.id,0xF7]:
            message.append(each)

        while (self.stereo == -1):
            self.connection.output.write_sys_ex(msg = message,when=midi.time())
            time.sleep(0.005) #waiting for the mixer as searching for a response immediately often is does not allow enough time for the mixer to respond
            try:
                self.stereo = Parser.listenFor(self.connection,sysExChg,toStereo,self.id)[4]
            except ResponseException as e:
                pass

    def select(self,cc):
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x10,0x3E,0x7F,0x01,0x22,0x00,cc,0x00,0x00,0x00,0x01,0xf7],when=midi.time())

    def draw(self,context,pos):
        """draws a meter for given input"""
        
        segment = 0
        for i in range (884,self.level, 200):
            if (i>4096):
                break
            segment += 1
            if i < 3000: 
                pygame.draw.rect(context, (0, 192, 0), (pos[0]+18, pos[1]-(segment*5)+5, 5, 4))
            elif i >= 3000 and i < 3899:
                pygame.draw.rect(context, (250, 200, 0), (pos[0]+18, pos[1]-(segment*5)+5, 5, 4))
            else:
                pygame.draw.rect(context, (255, 0, 0), (pos[0]+18, pos[1]-(segment*5)+5, 5, 4))