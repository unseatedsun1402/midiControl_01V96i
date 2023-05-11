"""Yamaha digital mixer virtual input channel object"""
import Connection, VU
import time
import pygame.midi as midi
import pygame

sysExChg = [0xF0,0x43,0x10,0x3E]
sysExReq = [0xf0,0x43,0x30,0x3e]

class inputChannel():
    """Yamaha digital mixer virtual input channel object"""
    connection = Connection

    def __init__(self,val: int,conn: Connection):
        """Pass an integer value to identify the channel"""
        self.connection = conn
        self.id = val
        self.level = 0
        try:
            if self.id<32:
                self.short = self.__get_short()
                self.name = self.__get_name()
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
        msg = [0xF0,0x43,0x30,0x3E,0x1A,0x02,0x04,0x00,self.id]
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
        self.connection.output.write_sys_ex(msg = [0xF0,0x43,0x30,0x3E,0x1A,0x04,0x50,0x00,self.id,0xf7],when=midi.time())

    def update_level(self,data):
        self.level = ((16*data[2])+data[3])
        return True
    
    def draw(self,context):
        """draws a meter for given input"""
        for i in range (0,self.level, 6):
            if i < 20: 
                pygame.draw.rect(context, (0, 192, 0), (self.id*10, (475-(i)), 10, 5))
            elif i >= 20 and i < 30:
                pygame.draw.rect(context, (255, 255, 0), (self.id*10, (475-(i)), 10, 5))
            else:
                pygame.draw.rect(context, (255, 0, 0), (self.id*10, (475-(i)), 10, 5))